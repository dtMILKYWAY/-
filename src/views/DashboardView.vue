<template>
  <div class="dashboard-container">
    <!-- 第一行：数据卡片 -->
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="6">
        <div class="card-item bg-blue">
          <div class="content">
            <div class="text">总员工数</div>
            <div class="num">{{ stats.total_users }}</div>
          </div>
          <el-icon><User /></el-icon>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="card-item bg-green">
          <div class="content">
            <div class="text">部门总数</div>
            <div class="num">{{ stats.total_departments }}</div>
          </div>
          <el-icon><OfficeBuilding /></el-icon>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="card-item bg-orange">
          <div class="content">
            <div class="text">待办事项</div>
            <div class="num">8 <span class="small-text">项</span></div>
          </div>
          <el-icon><Warning /></el-icon>
        </div>
      </el-col>
       <el-col :span="6">
        <div class="card-item bg-purple">
          <div class="content">
            <div class="text">我的项目</div>
            <div class="num">3 <span class="small-text">个</span></div>
          </div>
          <el-icon><Briefcase /></el-icon>
        </div>
      </el-col>
    </el-row>

    <!-- 第二行：图表和快速开始 -->
    <el-row :gutter="20">
      <el-col :span="16">
        <div class="chart-wrapper">
          <h3>各部门人数分布</h3>
          <v-chart class="chart" :option="chartOption" autoresize />
        </div>
      </el-col>
      <el-col :span="8">
        <div class="chart-wrapper quick-start-wrapper">
          <h3>快速开始</h3>
          <el-row :gutter="10">
            <el-col :span="12">
              <div class="action-item bg-blue-light">
                <el-icon><EditPen /></el-icon>
                <span>发起审批</span>
              </div>
            </el-col>
            <el-col :span="12">
               <div class="action-item bg-green-light">
                <el-icon><Notification /></el-icon>
                <span>发布公告</span>
              </div>
            </el-col>
            <el-col :span="12">
               <div class="action-item bg-orange-light">
                <el-icon><Calendar /></el-icon>
                <span>我的日程</span>
              </div>
            </el-col>
            <el-col :span="12">
               <div class="action-item bg-purple-light">
                <el-icon><DataAnalysis /></el-icon>
                <span>查看报告</span>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, reactive } from 'vue';
import { getDashboardData } from '@/api';
import { ElMessage } from 'element-plus';
import { User, OfficeBuilding, Warning, Briefcase, EditPen, Notification, Calendar, DataAnalysis } from '@element-plus/icons-vue';
import * as echarts from 'echarts/core';
import { PieChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import VChart from 'vue-echarts';

echarts.use([TitleComponent, TooltipComponent, LegendComponent, GridComponent, PieChart, CanvasRenderer]);

const loading = ref(true);
const stats = reactive({ total_users: 0, total_departments: 0 });
const departmentDistribution = ref<any[]>([]);

const chartOption = computed(() => ({
  tooltip: { trigger: 'item', formatter: '{b}: {c} 人 ({d}%)' },
  legend: { orient: 'vertical', left: 'left', top: 'center' },
  series: [{
    name: '部门人数',
    type: 'pie',
    radius: ['50%', '70%'],
    data: departmentDistribution.value,
    itemStyle: { borderRadius: 5, borderColor: '#fff', borderWidth: 2 },
  }],
}));

onMounted(async () => {
  loading.value = true;
  try {
    const res = await getDashboardData();
    stats.total_users = res.data.stats.total_users;
    stats.total_departments = res.data.stats.total_departments;
    departmentDistribution.value = res.data.department_distribution.map(item => ({
      name: item.name,
      value: item.employee_count,
    }));
  } catch (error) {
    ElMessage.error('获取仪表盘数据失败');
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.dashboard-container { display: flex; flex-direction: column; gap: 20px; }
.stats-cards .card-item {
    color: white; border-radius: 8px; padding: 25px;
    display: flex; justify-content: space-between; align-items: center;
    transition: all 0.3s; cursor: pointer;
}
.stats-cards .card-item:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
.card-item .el-icon { font-size: 50px; opacity: 0.3; }
.card-item .content { text-align: left; }
.card-text { font-size: 16px; margin-bottom: 10px; }
.card-num { font-size: 30px; font-weight: bold; }
.small-text { font-size: 16px; font-weight: normal; margin-left: 5px; }
.bg-blue { background: #409EFF; }
.bg-green { background: #67C23A; }
.bg-orange { background: #E6A23C; }
.bg-purple { background: #626aef; }

.chart-wrapper { background-color: #fff; padding: 20px; border-radius: 8px; height: 440px; }
.chart { height: 350px; }
h3 { margin: 0 0 20px 0; font-size: 18px; font-weight: 600; }
.quick-actions {
    display: flex;
    flex-direction: column;
    gap: 15px;
}
.quick-actions .el-button {
    width: 100%;
    height: 50px;
    font-size: 16px;
}
.quick-start-wrapper h3 {
  margin-bottom: 30px; /* 增加标题和内容间距 */
}
.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 120px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 10px;
}
.action-item:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.action-item .el-icon {
  font-size: 32px;
  margin-bottom: 10px;
}
.action-item span {
  font-size: 16px;
}
.bg-blue-light { background-color: #ecf5ff; color: #409eff; }
.bg-green-light { background-color: #f0f9eb; color: #67c23a; }
.bg-orange-light { background-color: #fdf6ec; color: #e6a23c; }
.bg-purple-light { background-color: #f0f0ff; color: #626aef; }
</style>