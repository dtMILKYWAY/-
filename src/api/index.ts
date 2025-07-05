// frontend/src/api/index.ts

import axios from 'axios';
import { useUserStore } from '@/stores/user';

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

// 请求拦截器 (这部分是正确的，保持不变)
apiClient.interceptors.request.use(
  (config) => {
    const userStore = useUserStore();
    const token = userStore.token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ======================= 核心修正：添加缺失的函数 =======================
// 获取当前登录用户的信息
export const getUserInfo = () => apiClient.get('/user/info/');
// ====================================================================

// 登录接口
export const login = (data: any) => apiClient.post('/token/', data);

// 获取部门列表
export const getDepartments = () => apiClient.get('/departments/');

// 创建新部门
export const createDepartment = (data: any) => apiClient.post('/departments/', data);

// 更新部门信息
export const updateDepartment = (id: number, data: any) => apiClient.put(`/departments/${id}/`, data);

// 删除部门
export const deleteDepartment = (id: number) => apiClient.delete(`/departments/${id}/`);

// 获取用户列表
export const getUsers = (params?: object) => apiClient.get('/users/', { params });

// 创建新用户 (直接用 users/ 接口的 POST)
export const createUser = (data: any) => apiClient.post('/users/', data);

// 更新用户信息
export const updateUser = (uid: string, data: any) => apiClient.patch(`/users/${uid}/`, data); // 使用 PATCH 更佳

// 删除用户
export const deleteUser = (uid: string) => apiClient.delete(`/users/${uid}/`);

// 获取仪表盘统计数据
export const getDashboardData = () => apiClient.get('/dashboard/data/');

// 获取管理员列表
export const getManagers = () => apiClient.get('/managers/'); // 指向新的 URL

export default apiClient;