<template>
  <el-container class="main-layout">
    <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar">
      <div class="sidebar-logo">
        <img src="/logo.png" alt="Logo" />
        <span v-if="!isCollapse">OA 平台</span>
      </div>
      <!-- 导航菜单 -->
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical"
        :collapse="isCollapse"
        router
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataLine /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-sub-menu index="/management">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/management/departments">
            <el-icon><OfficeBuilding /></el-icon>
            <span>部门管理</span>
          </el-menu-item>
          <el-menu-item index="/management/users">
            <el-icon><User /></el-icon>
            <span>员工管理</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="header-left">
           <el-icon class="collapse-icon" @click="toggleSidebar"><Fold /></el-icon>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="el-dropdown-link">
              欢迎您, {{userStore.username}}
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人中心</el-dropdown-item>
                <el-dropdown-item>修改密码</el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main-content">
        <!-- 子路由的出口 -->
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';
import {
  DataLine, Setting, OfficeBuilding, User, Fold, ArrowDown
} from '@element-plus/icons-vue';

const isCollapse = ref(false);
const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const activeMenu = computed(() => route.path);

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value;
};

const handleLogout = () => {
  userStore.logout();
  router.push('/login');
}
</script>

<style scoped>
.main-layout {
  height: 100vh;
}
.sidebar {
  background-color: #001529;
  transition: width 0.3s;
}
.sidebar-logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  font-weight: 600;
}
.sidebar-logo img {
  width: 32px;
  height: 32px;
  margin-right: 10px;
}
.el-menu-vertical {
  border-right: none;
  background-color: #001529;
}
.el-menu-vertical:not(.el-menu--collapse) {
  width: 200px;
}
.el-menu-item, :deep(.el-sub-menu__title) {
  color: #a6adb4;
}
.el-menu-item:hover, :deep(.el-sub-menu__title:hover) {
  background-color: #000c17 !important;
}
.el-menu-item.is-active {
  color: white !important;
  background-color: #1890ff !important;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e4e7ed;
  background-color: white;
}
.collapse-icon {
  font-size: 24px;
  cursor: pointer;
}
.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>