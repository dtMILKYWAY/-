<template>
  <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px" @closed="handleClose" append-to-body>
    <el-form ref="formRef" :model="formData" :rules="formRules" label-width="120px">
      <el-form-item label="部门名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入部门名称" />
      </el-form-item>
      <el-form-item label="部门简介" prop="intro">
        <el-input v-model="formData.intro" type="textarea" placeholder="请输入部门简介" />
      </el-form-item>
      <el-form-item label="部门主管 (Leader)" prop="leader">
        <el-input v-model="formData.leader" placeholder="请输入主管姓名（手动输入）" />
      </el-form-item>
      <el-form-item label="上级分管 (Manager)" prop="manager">
        <el-select v-model="formData.manager" placeholder="请选择分管领导" filterable clearable>
          <el-option v-for="user in managerList" :key="user.uid" :label="user.realname" :value="user.uid" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="handleSubmit(formRef)" :loading="loading">确 定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';
import { ElMessage } from 'element-plus';
import { getManagers, createDepartment, updateDepartment } from '@/api';

interface Manager { uid: string; realname: string; }

const emit = defineEmits(['success']);

const dialogVisible = ref(false);
const loading = ref(false);
const dialogTitle = ref('');
const formRef = ref<FormInstance>();
const managerList = ref<Manager[]>([]);

const formData = reactive({
  id: null as number | null,
  name: '',
  intro: '',
  leader: '',
  manager: null as string | null, // manager 存储的是 uid
});

const formRules = reactive<FormRules>({
  name: [{ required: true, message: '部门名称不能为空', trigger: 'blur' }],
});

const fetchManagers = async () => {
    try {
        const res = await getManagers();
        managerList.value = res.data;
    } catch (error) { console.error("获取管理员列表失败", error); }
}
onMounted(fetchManagers);

const open = (isEdit = false, data: any = {}) => {
  dialogVisible.value = true;
  if (isEdit) {
    dialogTitle.value = '编辑部门';
    // 回填数据，确保 manager 字段被正确赋值为 manager 的 uid
    Object.assign(formData, { ...data, manager: data.manager?.uid || null });
  } else {
    dialogTitle.value = '新增部门';
  }
};
defineExpose({ open });

const handleSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        // 直接提交 formData 即可。
        // 因为 formData.manager 中存储的就是我们选择的 uid，
        // 这正好是后端 PrimaryKeyRelatedField 期望接收的数据。
        if (formData.id) {
          await updateDepartment(formData.id, formData);
          ElMessage.success('更新成功！');
        } else {
          await createDepartment(formData);
          ElMessage.success('新增成功！');
        }
        emit('success');
        dialogVisible.value = false;
      } catch (error) {
        ElMessage.error('操作失败');
      } finally {
        loading.value = false;
      }
    }
  });
};

const handleClose = () => {
    formRef.value?.resetFields();
    formData.id = null;
}
</script>

<style scoped> .el-select { width: 100%; } </style>