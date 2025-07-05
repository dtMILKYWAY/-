<template>
  <div class="department-management">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">部门管理</h1>
      <el-button type="primary" :icon="Plus" @click="handleCreate">新增部门</el-button>
    </div>

    <!-- 数据表格 -->
    <el-table :data="departments" v-loading="loading" style="width: 100%" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="部门名称" />
      <el-table-column prop="intro" label="部门简介" />
      <el-table-column prop="leader" label="部门主管 (Leader)">
        <template #default="scope">{{ scope.row.leader || '未指定' }}</template>
      </el-table-column>
      <el-table-column prop="manager.realname" label="上级分管 (Manager)">
        <template #default="scope">{{ scope.row.manager?.realname || '未指定' }}</template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="scope">
          <el-button size="small" type="primary" :icon="Edit" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" :icon="Delete" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 弹窗组件 -->
    <DepartmentDialog ref="dialogRef" @success="fetchDepartments" />
    <ConfirmDialog ref="confirmDialogRef" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getDepartments, deleteDepartment as deleteApi } from '@/api';
import { ElMessage } from 'element-plus';
import { Plus, Edit, Delete } from '@element-plus/icons-vue';
import DepartmentDialog from '@/components/DepartmentDialog.vue';
import ConfirmDialog from '@/components/ConfirmDialog.vue';

interface Department {
  id: number;
  name: string;
  intro: string;
  leader: string | null;
  manager: { uid: string; realname: string } | null;
}

const departments = ref<Department[]>([]);
const loading = ref(true);
const dialogRef = ref();
const confirmDialogRef = ref();

const fetchDepartments = async () => {
  loading.value = true;
  try {
    const res = await getDepartments();
    departments.value = res.data;
  } catch (error) {
    ElMessage.error('获取部门列表失败');
  } finally {
    loading.value = false;
  }
};
onMounted(fetchDepartments);

const handleCreate = () => {
  dialogRef.value?.open();
};

const handleEdit = (row: Department) => {
  dialogRef.value?.open(true, row);
};

const handleDelete = (row: Department) => {
  confirmDialogRef.value?.open({
    title: '删除确认',
    message: `您确定要永久删除部门 "${row.name}" 吗？`,
    type: 'warning',
    confirmButtonText: '确认删除',
    onConfirm: async () => {
      try {
        await deleteApi(row.id);
        ElMessage.success('删除成功！');
        fetchDepartments();
      } catch (error: any) {
        const errorMessage = error.response?.data?.detail || '删除失败，请稍后重试';
        ElMessage.error(errorMessage);
        throw error;
      }
    }
  });
};
</script>

<style scoped>
.department-management { padding: 20px; background-color: #fff; border-radius: 8px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-title { font-size: 24px; font-weight: 600; color: #303133; }
</style>