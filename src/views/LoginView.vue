<template>
  <div class="login-container">
    <!-- 左侧品牌展示区 -->
    <div class="left-panel">
      <div class="brand-content">
        <svg class="brand-logo" width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 17L12 22L22 17" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 12L12 17L22 12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1 class="brand-title">企业协同办公平台</h1>
        <p class="brand-subtitle">赋能高效协作，激发无限潜能。我们的平台集成了项目管理、即时通讯和知识库，为您提供一站式解决方案。</p>
      </div>
    </div>

    <!-- 右侧登录表单区 -->
    <div class="right-panel">
      <div class="login-form-wrapper">
        <h2>欢迎回来</h2>
        <p class="welcome-text">请输入您的邮箱和密码以登录系统</p>
        <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" size="large" @keyup.enter="handleLogin(loginFormRef)">
          <el-form-item prop="email">
            <el-input v-model="loginForm.email" placeholder="邮箱" :prefix-icon="User"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="loginForm.password" type="password" placeholder="密码" show-password :prefix-icon="Lock"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button class="login-button" type="primary" @click="handleLogin(loginFormRef)" :loading="loading">
              安全登录
            </el-button>
          </el-form-item>
        </el-form>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import {ElMessageBox, type FormInstance, type FormRules} from 'element-plus';
import { ElMessage } from 'element-plus';
import { User, Lock } from '@element-plus/icons-vue';
import { useUserStore } from '@/stores/user'; // 使用别名路径
const router = useRouter();
const userStore = useUserStore();

const loginFormRef = ref<FormInstance>();
const loading = ref(false);

const loginForm = reactive({
  email: '',
  password: '',
});

const loginRules = reactive<FormRules>({
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] },
  ],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
});

// frontend/src/views/LoginView.vue -> handleLogin()
const handleLogin = async (formEl: FormInstance | undefined) => {
  if (!formEl || loading.value) return;
  try {
    await formEl.validate();
    loading.value = true;
    // 只调用一个 action，所有复杂逻辑都在 store 里
    await userStore.login(loginForm);
    ElMessage.success('登录成功！');
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || '登录失败，请检查凭据或权限';
    ElMessageBox.alert(errorMessage, '登录失败', { /* ... */ });
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* ... 你已有的所有样式保持不变 ... */
.login-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  background-color: #ffffff;
}

.left-panel {
  width: 55%;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: white;
}

.brand-content {
  max-width: 480px;
  text-align: left;
}

.brand-logo {
  margin-bottom: 40px;
  opacity: 0.8;
}

.brand-title {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 24px 0;
}

.brand-subtitle {
  font-size: 1.125rem;
  font-weight: 300;
  line-height: 1.6;
  opacity: 0.8;
}

.right-panel {
  width: 45%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-form-wrapper {
  width: 380px;
}

h2 {
  font-size: 2.25rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
}

.welcome-text {
  color: #6b7280;
  margin-bottom: 40px;
  font-size: 1rem;
}

.login-button {
  width: 100%;
  height: 52px;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 8px;
  letter-spacing: 1px;
}

:deep(.el-input__wrapper) {
  height: 52px;
  border-radius: 8px;
}

</style>