from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.oaauth.serializers import MyTokenObtainPairSerializer
from applications.oaauth import views
# 导入 Simple JWT 提供的视图
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# 1. 创建路由器并注册你的视图集
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'departments', views.DepartmentViewSet, basename='department')

# 2. 定义 urlpatterns
urlpatterns = [
    # 添加获取用户信息的 URL
    path('api/user/info/', views.UserInfoView.as_view(), name='user_info'),
    path('admin/', admin.site.urls),

    # 3. 将路由器生成的 URL 包含进来，并加上 'api/' 前缀
    path('api/', include(router.urls)),
    path('api/register/', views.UserRegisterView.as_view(), name='user_register'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/data/', views.DashboardDataView .as_view(), name='dashboard_data'),
    path('api/managers/', views.ManagerListView.as_view(), name='manager_list'),
]