from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from .models import OAUser, OADepartment


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAUser
        fields = ['uid', 'realname']


class DepartmentSerializer(serializers.ModelSerializer):
    """部门序列化器（最终完美版）"""
    # --- “读”操作配置 ---
    # manager_info 字段只用于读取，它通过 source='manager' 获取 manager 对象，
    # 并用 SimpleUserSerializer 进行序列化。
    manager_info = SimpleUserSerializer(source='manager', read_only=True)

    class Meta:
        model = OADepartment
        # 在 fields 中，我们只包含模型的真实字段
        # leader 是 CharField，会被自动处理
        fields = ['id', 'name', 'intro', 'leader', 'manager', 'manager_info']

        # --- “写”操作配置 ---
        # extra_kwargs 允许我们为特定字段在写入时指定特殊的序列化器
        extra_kwargs = {
            # manager 字段在写入时，被视为一个只写的主键字段
            'manager': {'write_only': True, 'required': False},
        }

    # (可选但推荐) 重写 to_representation 方法，让 API 输出更干净
    def to_representation(self, instance):
        # 先获取标准的 representation
        ret = super().to_representation(instance)
        # 将嵌套的 manager_info 赋值给 manager 字段
        ret['manager'] = ret.pop('manager_info', None)
        return ret


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器（最终修正版）"""
    # "读"操作时，嵌套显示部门信息
    department = DepartmentSerializer(read_only=True)
    # "写"操作时，允许前端传入一个名为 'department_id' 的字段
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=OADepartment.objects.all(),
        source='department',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = OAUser
        fields = [
            'uid', 'realname', 'email', 'password', 'telephone',
            'department', 'department_id', 'is_staff', 'status', 'is_active', 'date_joined'
        ]
        # password 字段只用于写入，不用于读出
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def create(self, validated_data):
        if 'department' not in validated_data:
            validated_data.pop('department', None)
        user = OAUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # 1. 首先，调用父类的 validate，完成邮箱和密码的基础验证
        # 如果这里验证失败，会直接抛出异常，后面的代码不会执行
        data = super().validate(attrs)

        # 2. 基础验证通过后，我们拿到了 self.user 对象
        user = self.user

        # 3. 在这里实现我们自己的、更复杂的权限检查

        # 检查条件1：用户是否是 staff (管理员)
        is_manager_staff = user.is_staff

        # 检查条件2：用户是否是任何一个部门的 Leader
        # 我们用用户的真实姓名去 OADepartment 表里反查
        is_department_leader = OADepartment.objects.filter(leader=user.realname).exists()

        # 4. 最终判断：只要满足以上任一条件，就允许登录
        if not (is_manager_staff or is_department_leader):
            # 如果两个条件都不满足，则引发认证失败的异常
            raise serializers.ValidationError(
                _("登录失败：您的账户没有访问该系统的权限。"),
                code='authorization',
            )

        # 5. 如果权限检查通过，在 token 中添加自定义信息
        data['realname'] = user.realname
        data['email'] = user.email

        return data

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAUser
        fields = ['realname', 'email', 'password', 'department', 'status', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = OAUser.objects.create_user(**validated_data)
        return user