<template>
  <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px" @closed="handleClose" append-to-body>
    <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
      <el-form-item label="真实姓名" prop="realname">
        <el-input v-model="formData.realname" placeholder="请输入员工姓名" />
      </el-form-item>
      <el-form-item label="邮箱地址" prop="email">
        <el-input v-model="formData.email" placeholder="将作为登录凭据" :disabled="isEdit" />
      </el-form-item>
      <el-form-item v-if="!isEdit" label="初始密码" prop="password">
        <el-input v-model="formData.password" type="password" show-password placeholder="不填写则默认为 111111" />
      </el-form-item>
      <el-form-item label="所属部门" prop="department_id">
        <el-select v-model="formData.department_id" placeholder="请选择所属部门" clearable>
          <el-option v-for="dept in departmentList" :key="dept.id" :label="dept.name" :value="dept.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="管理员权限" prop="is_staff">
        <el-switch v-model="formData.is_staff" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit(formRef)" :loading="loading">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';
import { ElMessage } from 'element-plus';
import { getDepartments, createUser as createUserApi, updateUser as updateUserApi } from '@/api';

interface Department { id: number; name: string; }

const emit = defineEmits(['success']);
const dialogVisible = ref(false);
const loading = ref(false);
const isEdit = ref(false);
const formRef = ref<FormInstance>();
const departmentList = ref<Department[]>([]);

const dialogTitle = computed(() => isEdit.value ? '编辑员工' : '新增员工');

const formData = reactive({
  uid: null as string | null,
  realname: '',
  email: '',
  password: '',
  department_id: null as number | null,
  is_staff: false,
});

// 密码在新增时是必需的，但可以有默认值
const formRules = reactive<FormRules>({
  realname: [{ required: true, message: '姓名不能为空', trigger: 'blur' }],
  email: [{ required: true, message: '邮箱不能为空', trigger: 'blur' }, { type: 'email' }],
});

onMounted(async () => {
  try { departmentList.value = (await getDepartments()).data; } catch (error) { console.error(error); }
});

const open = (edit = false, data: any = {}) => {
  dialogVisible.value = true;
  isEdit.value = edit;
  if (edit) {
    Object.assign(formData, { ...data, department_id: data.department?.id || null });
  }
};
defineExpose({ open });

const handleSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid) => {
    if (valid) {
      loading.value = true;
       try {
            // 只构建后端需要的字段
            const payload: any = {
                realname: formData.realname,
                email: formData.email,
                is_staff: formData.is_staff,
            };
            // 只有当部门被选择时，才添加 department_id
            if (formData.department_id) {
                payload.department_id = formData.department_id;
            }
            if (isEdit.value) {
                await updateUserApi(formData.uid!, payload);
                ElMessage.success('更新成功！');
            } else {
                // 新增时才需要密码
                payload.password = formData.password || '111111';
                await createUserApi(payload);
                ElMessage.success('新增员工成功！');
            }
        emit('success');
        dialogVisible.value = false;
      } catch (error: any) {
        const msg = error.response?.data?.email?.[0] || '操作失败';
        ElMessage.error(msg);
      } finally { loading.value = false; }
    }
  });
};

const handleClose = () => {
  formRef.value?.resetFields();
  formData.uid = null;
}
</script>

<style scoped> .el-select { width: 100%; } </style>