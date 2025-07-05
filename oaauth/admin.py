# applications/oaauth/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import OAUser, OADepartment

@admin.register(OAUser)
class OAUserAdmin(UserAdmin):
    # 在列表页中显示的字段
    list_display = ('email', 'realname', 'department', 'is_staff', 'is_active', 'date_joined')
    # 搜索字段
    search_fields = ('email', 'realname')
    # 过滤器
    list_filter = ('is_staff', 'is_active', 'department')
    # 自定义编辑页面的字段布局
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('个人信息', {'fields': ('realname', 'telephone', 'department')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    # 新增用户页面需要的字段
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'realname', 'department', 'password', 'password2'),
        }),
    )
    ordering = ('-date_joined',)

@admin.register(OADepartment)
class OADepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'intro', 'leader', 'manager')
    search_fields = ('name',)
    autocomplete_fields = ['manager'] # Manager 字段使用搜索框，而不是下拉列表