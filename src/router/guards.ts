// frontend/src/router/guards.ts
import type { Router } from 'vue-router'
import { useUserStore } from '../stores/user'

export function createRouterGuards(router: Router) {
  router.beforeEach(async (to, _from, next) => {
    const userStore = useUserStore();
    const token = userStore.token;

    // 如果要去的地方不是登录页，并且没有 token
    if (to.name !== 'Login' && !token) {
      // 重定向到登录页
      next({ name: 'Login' });
    }
    // 如果要去的地方是登录页，并且已经有 token 了
    else if (to.name === 'Login' && token) {
      // 直接跳转到首页
      next({ path: '/' });
    }
    else {
      // 其他情况，正常放行
      next();
    }
  });
}