from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import OAUser, OADepartment
from .serializers import UserSerializer, DepartmentSerializer, SimpleUserSerializer, UserRegisterSerializer
from django.db.models import Count
from .serializers import SimpleUserSerializer

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(ModelViewSet):
    """用于管理员工信息的 API 视图集"""
    queryset = OAUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['realname', 'email', 'telephone']
    def get_queryset(self):
        """
        重写 get_queryset 方法，实现数据权限控制 (最终修正版)。
        """
        user = self.request.user

        # 1. 如果是超级用户或管理员，返回所有用户
        if user.is_superuser or user.is_staff:
            return OAUser.objects.all().order_by('-date_joined')

        # 2. 检查当前用户是不是某个部门的 Leader
        # 直接用用户的真实姓名去 OADepartment 表的 leader 字段里查询
        led_departments = OADepartment.objects.filter(leader=user.realname)

        if led_departments.exists():
            # 3. 如果是 Leader，只返回他所领导的这些部门下的所有员工
            return OAUser.objects.filter(department__in=led_departments).order_by('-date_joined')

        # 4. 如果什么都不是，返回空
        return OAUser.objects.none()

class DepartmentViewSet(ModelViewSet):
    queryset = OADepartment.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class UserRegisterView(generics.CreateAPIView):
    """
    用户注册/新增员工接口
    """
    queryset = OAUser.objects.all()
    serializer_class = UserRegisterSerializer
    # 注意：这个接口的权限必须是 IsAuthenticated，
    # 这样只有已登录的管理员才能调用它来新增员工。
    permission_classes = [IsAuthenticated]


class DashboardDataView(APIView):
    """
    为仪表盘提供核心统计数据 (最终简化版)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_users = OAUser.objects.count()
        total_departments = OADepartment.objects.count()

        department_distribution = (
            OADepartment.objects
            .annotate(employee_count=Count('staffs'))
            .values('name', 'employee_count')
        )

        data = {
            'stats': {
                'total_users': total_users,
                'total_departments': total_departments,
            },
            'department_distribution': list(department_distribution)
        }
        return Response(data)


class ManagerListView(generics.ListAPIView):
    """
    一个只读的 API 端点，专门用于返回管理员 (is_staff=True) 列表。
    """
    queryset = OAUser.objects.filter(is_staff=True)
    serializer_class = SimpleUserSerializer
    permission_classes = [IsAuthenticated] # 只需要登录即可访问