// frontend/src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

// 使用统一的 @ 别名
import MainLayout from '@/layout/MainLayout.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'), // 使用 @
    meta: { title: '登录' }
  },
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/DashboardView.vue'), // 使用 @
        meta: { title: '仪表盘' }
      },
      {
        path: 'management/departments',
        name: 'DepartmentManagement',
        component: () => import('@/views/DepartmentView.vue'), // 使用 @
        meta: { title: '部门管理' }
      },
      {
        path: 'management/users',
        name: 'UserManagement',
        component: () => import('@/views/UserView.vue'), // 使用 @
        meta: { title: '员工管理' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue') // 使用 @
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token');

  if (to.name !== 'Login' && !token) {
    // 如果要去受保护的页面，但没有 token，则去登录
    next({ name: 'Login' });
  } else if (to.name === 'Login' && token) {
    // 如果已经登录了，还想去登录页，则直接送回首页
    next('/');
  } else {
    // 其他所有情况，一律放行！
    next();
  }
});

export default router;