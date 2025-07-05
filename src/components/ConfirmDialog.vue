<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="400px"
    append-to-body
    align-center
  >
    <div class="confirm-content">
      <el-icon :size="24" class="icon" :color="iconColor">
        <component :is="iconComponent" />
      </el-icon>
      <p>{{ message }}</p>
    </div>
    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button :type="type" @click="handleConfirm" :loading="loading">
        {{ confirmButtonText }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { QuestionFilled, WarningFilled, CircleCheckFilled, CircleCloseFilled } from '@element-plus/icons-vue';

type DialogType = 'warning' | 'info' | 'success' | 'error';

const dialogVisible = ref(false);
const loading = ref(false);
const title = ref('提示');
const message = ref('');
const type = ref<DialogType>('warning');
const confirmButtonText = ref('确定');

let onConfirm: () => Promise<void>;

const open = (options: {
  title: string;
  message: string;
  type: DialogType;
  confirmButtonText?: string;
  onConfirm: () => Promise<void>;
}) => {
  title.value = options.title;
  message.value = options.message;
  type.value = options.type;
  confirmButtonText.value = options.confirmButtonText || '确定';
  onConfirm = options.onConfirm;
  dialogVisible.value = true;
};
defineExpose({ open });

const iconComponent = computed(() => {
    switch(type.value) {
        case 'warning': return WarningFilled;
        case 'success': return CircleCheckFilled;
        case 'error': return CircleCloseFilled;
        default: return QuestionFilled;
    }
});

const iconColor = computed(() => {
    switch(type.value) {
        case 'warning': return '#E6A23C';
        case 'success': return '#67C23A';
        case 'error': return '#F56C6C';
        default: return '#909399';
    }
})

const handleConfirm = async () => {
  loading.value = true;
  try {
    await onConfirm();
    dialogVisible.value = false;
  } finally {
    loading.value = false;
  }
};

const handleCancel = () => {
  dialogVisible.value = false;
};
</script>

<style scoped>
.confirm-content {
  display: flex;
  align-items: center;
  gap: 16px;
}
.icon {
  flex-shrink: 0;
}
p {
  margin: 0;
  font-size: 1rem;
  color: #606266;
}
</style>