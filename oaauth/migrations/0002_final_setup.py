# applications/oaauth/migrations/0002_final_setup.py

from django.db import migrations
from django.contrib.auth.hashers import make_password
import random


def final_setup(apps, schema_editor):
    """
    1. 创建基础部门
    2. 创建核心用户（管理员和主管）
    3. 为部门设置负责人
    4. 创建角色组并分配权限
    5. 将主管加入角色组
    6. 生成海量随机员工数据
    """
    # 导入需要的模型
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    OAUser = apps.get_model('oaauth', 'OAUser')
    OADepartment = apps.get_model('oaauth', 'OADepartment')

    try:
        from faker import Faker
        fake = Faker('zh_CN')
    except ImportError:
        fake = None

    print("\n--- [OA系统] 开始执行最终数据初始化 ---")

    # --- 步骤 1: 创建基础部门 ---
    print("  -> 正在创建基础部门...")
    depts_data = [
        {'name': '董事会', 'intro': '董事会'},
        {'name': '产品开发部', 'intro': '产品设计，技术开发'},
        {'name': '运营部', 'intro': '客户运营，产品运营'},
        {'name': '销售部', 'intro': '销售产品'},
        {'name': '人事部', 'intro': '员工招聘，员工培训，员工考核'},
        {'name': '财务部', 'intro': '财务报表，财务审核'},
    ]
    for data in depts_data:
        OADepartment.objects.update_or_create(name=data['name'], defaults=data)

    boarder = OADepartment.objects.get(name='董事会')
    developer = OADepartment.objects.get(name='产品开发部')
    operator = OADepartment.objects.get(name='运营部')
    saler = OADepartment.objects.get(name='销售部')
    hr = OADepartment.objects.get(name='人事部')
    finance = OADepartment.objects.get(name='财务部')
    print("     基础部门创建完毕。")

    # --- 步骤 2: 创建核心用户 ---
    print("  -> 正在创建核心用户...")
    core_users_data = [
        {'email': 'dongdong@qq.com', 'realname': '东东', 'department': boarder, 'is_staff': True, 'is_superuser': True},
        {'email': 'duoduo@qq.com', 'realname': '多多', 'department': boarder, 'is_staff': True, 'is_superuser': True},
        {'email': 'zhangsan@qq.com', 'realname': '张三', 'department': developer, 'is_staff': False},
        {'email': 'lisi@qq.com', 'realname': '李四', 'department': operator, 'is_staff': False},
        {'email': 'wangwu@qq.com', 'realname': '王五', 'department': hr, 'is_staff': False},
        {'email': 'zhaoliu@qq.com', 'realname': '赵六', 'department': finance, 'is_staff': False},
        {'email': 'sunqi@qq.com', 'realname': '孙七', 'department': saler, 'is_staff': False},
    ]
    for data in core_users_data:
        defaults = {k: v for k, v in data.items() if k != 'email'}
        defaults['password'] = make_password('111111')
        OAUser.objects.update_or_create(email=data['email'], defaults=defaults)

    dongdong = OAUser.objects.get(email="dongdong@qq.com")
    duoduo = OAUser.objects.get(email="duoduo@qq.com")
    zhangsan = OAUser.objects.get(email="zhangsan@qq.com")
    lisi = OAUser.objects.get(email="lisi@qq.com")
    wangwu = OAUser.objects.get(email="wangwu@qq.com")
    zhaoliu = OAUser.objects.get(email="zhaoliu@qq.com")
    sunqi = OAUser.objects.get(email="sunqi@qq.com")
    print("     核心用户创建完毕。")

    # --- 步骤 3: 为部门设置负责人 ---
    print("  -> 正在设置部门负责人...")
    boarder.leader = '张三';
    boarder.manager = None;
    boarder.save()
    developer.leader = '张三';
    developer.manager = dongdong;
    developer.save()
    operator.leader = '李四';
    operator.manager = dongdong;
    operator.save()
    saler.leader = '孙七';
    saler.manager = dongdong;
    saler.save()
    hr.leader = '王五';
    hr.manager = duoduo;
    hr.save()
    finance.leader = '赵六';
    finance.manager = duoduo;
    finance.save()
    print("     部门负责人设置完毕。")

    # --- 步骤 4: 创建角色组并分配权限 ---
    print("  -> 正在创建 '部门主管' 角色组...")
    leader_group, _ = Group.objects.get_or_create(name='部门主管')
    user_content_type = ContentType.objects.get_for_model(OAUser)
    user_permissions = Permission.objects.filter(content_type=user_content_type)
    leader_group.permissions.set(user_permissions)
    print("     '部门主管' 角色组已配置权限。")

    # --- 步骤 5: 将主管加入角色组 ---
    leader_names = OADepartment.objects.exclude(leader__isnull=True).exclude(leader='').values_list('leader',
                                                                                                    flat=True).distinct()
    leaders_to_add = OAUser.objects.filter(realname__in=leader_names, is_staff=False)
    leader_group.user_set.add(*leaders_to_add)
    print(f"     已将 {leaders_to_add.count()} 名主管加入角色组。")

    # --- 步骤 6: 生成海量随机员工数据 ---
    if fake:
        print("  -> 正在生成随机员工数据...")
        departments_for_staff = list(OADepartment.objects.exclude(name='董事会'))
        if departments_for_staff:
            users_to_create = []
            for _ in range(200):
                users_to_create.append(OAUser(
                    realname=fake.name(),
                    email=fake.unique.email(),
                    password=make_password('111111'),
                    department=random.choice(departments_for_staff)
                ))
            OAUser.objects.bulk_create(users_to_create, ignore_conflicts=True)
            print(f"     成功生成 {len(users_to_create)} 名随机员工。")

    print("--- [OA系统] 所有数据初始化完毕 ---")


class Migration(migrations.Migration):
    dependencies = [
        ('oaauth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(final_setup),
    ]