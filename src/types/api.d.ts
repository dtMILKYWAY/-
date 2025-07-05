// 仪表盘统计卡片的数据类型
export interface DashboardStats {
  total_users: number;
  total_departments: number;
  admin_users: number;
  new_hires: number;
}

// 部门分布图的数据项类型
export interface DepartmentDistributionItem {
  name: string;
  employee_count: number;
}

// 近期活动日志的数据项类型
export interface ActivityLogItem {
  user: string;
  action: string;
  object: string;
  time: string;
}
// 仪表盘统计卡片的数据类型
export interface DashboardStats {
  total_users: number;
  total_departments: number;
  // 添加下面这两个字段
  admin_users: number;
  new_hires: number;
}