<template>
  <div class="user-management">
    <div class="page-header">
      <h1 class="page-title">员工管理</h1>
      <div class="actions-wrapper">
        <el-input
          v-model="searchKeyword"
          placeholder="按姓名、邮箱搜索"
          clearable
          @clear="fetchUsers"
          @keyup.enter="handleSearch"
          class="search-input"
        >
          <template #append>
            <el-button :icon="Search" @click="handleSearch" />
          </template>
        </el-input>
        <el-button type="primary" :icon="Plus" @click="handleCreate">新增员工</el-button>
      </div>
    </div>

    <el-table :data="users" v-loading="loading" style="width: 100%" border>
      <el-table-column prop="uid" label="员工ID" width="120" />
      <el-table-column prop="realname" label="姓名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="department.name" label="所属部门">
        <template #default="scope">{{ scope.row.department?.name || '未分配' }}</template>
      </el-table-column>
      <el-table-column label="管理员" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.is_staff ? 'success' : 'info'">{{ scope.row.is_staff ? '是' : '否' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="scope">
          <el-button size="small" type="primary" :icon="Edit" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" :icon="Delete" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <UserDialog ref="dialogRef" @success="fetchUsers" />
    <ConfirmDialog ref="confirmDialogRef" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getUsers as getUsersApi, deleteUser as deleteApi } from '@/api';
import { ElMessage } from 'element-plus';
import { Plus, Edit, Delete, Search } from '@element-plus/icons-vue';
import UserDialog from '@/components/UserDialog.vue';
import ConfirmDialog from '@/components/ConfirmDialog.vue';

// 定义清晰的类型接口
interface Department { id: number; name: string; }
interface User {
  uid: string;
  realname: string;
  email: string;
  department: Department | null;
  is_staff: boolean;
}

const users = ref<User[]>([]); // 使用类型
const loading = ref(true);
const dialogRef = ref();
const confirmDialogRef = ref();
const searchKeyword = ref('');

const fetchUsers = async () => {
  loading.value = true;
  try {
    const params: { search?: string } = {};
    if (searchKeyword.value) params.search = searchKeyword.value;
    users.value = (await getUsersApi(params)).data;
  } catch (error) { ElMessage.error('获取员工列表失败'); }
  finally { loading.value = false; }
};
onMounted(fetchUsers);

const handleSearch = () => fetchUsers();
const handleCreate = () => dialogRef.value?.open();
const handleEdit = (row: User) => dialogRef.value?.open(true, row);

const handleDelete = (row: User) => {
  confirmDialogRef.value?.open({
    title: '删除员工',
    message: `确定要删除员工 "${row.realname}" 吗？`,
    type: 'warning',
    onConfirm: async () => {
      try {
        await deleteApi(row.uid);
        ElMessage.success('删除成功！');
        fetchUsers();
      } catch (error) { ElMessage.error('删除失败'); throw error; }
    }
  });
};
</script>

<style scoped>
.user-management { padding: 20px; background-color: #fff; border-radius: 8px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-title { font-size: 24px; font-weight: 600; }
.actions-wrapper { display: flex; gap: 10px; }
.search-input { width: 240px; }
</style>