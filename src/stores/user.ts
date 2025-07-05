// frontend/src/stores/user.ts
import { defineStore } from 'pinia';
import { getUserInfo, login as loginApi } from '@/api';
import router from '@/router'; // 导入 router 实例

// ... UserInfo 接口定义 ...

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    userInfo: JSON.parse(localStorage.getItem('userInfo') || 'null'),
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    username: (state) => state.userInfo?.realname || '访客',
  },
  actions: {
    // 登录 Action：整合所有登录后操作
    async login(loginData: any) {
      const res = await loginApi(loginData);
      this.setTokenAndUser(res.data.access);
      // 登录成功后直接跳转
      await router.push('/');
    },

    // 登出 Action：整合所有登出操作
    logout() {
      this.token = null;
      this.userInfo = null;
      localStorage.removeItem('token');
      localStorage.removeItem('userInfo');
      // 登出后跳转到登录页
      router.push('/login');
    },

    // 核心函数：设置 Token 并获取用户信息
    async setTokenAndUser(token: string) {
      this.token = token;
      localStorage.setItem('token', token);
      // 设置 Axios 的默认请求头
      // apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // (更好的做法是在拦截器里做)

      // 立刻获取用户信息
      await this.fetchUserInfo();
    },

    // 获取用户信息
    async fetchUserInfo() {
      try {
        const res = await getUserInfo();
        this.userInfo = res.data;
        localStorage.setItem('userInfo', JSON.stringify(res.data));
      } catch (error) {
        console.error("获取用户信息失败，可能 Token 已过期", error);
        this.logout(); // 获取失败则强制登出
      }
    },
  },
});