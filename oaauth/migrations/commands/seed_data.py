# applications/oaauth/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from django.db import transaction
from applications.oaauth.models import OAUser, OADepartment
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = '使用基础数据填充数据库，此命令可安全地重复执行。'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('--- 开始填充基础数据 ---'))

        # --- 步骤 1: 创建部门 ---
        self.stdout.write('  -> 正在创建或更新部门...')
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
        self.stdout.write(self.style.SUCCESS('     部门数据已就绪。'))

        # 获取部门对象
        boarder = OADepartment.objects.get(name='董事会')
        developer = OADepartment.objects.get(name='产品开发部')
        operator = OADepartment.objects.get(name='运营部')
        saler = OADepartment.objects.get(name='销售部')
        hr = OADepartment.objects.get(name='人事部')
        finance = OADepartment.objects.get(name='财务部')

        # --- 步骤 2: 创建用户 ---
        self.stdout.write('  -> 正在创建或更新用户...')
        users_data = [
            {'email': 'dongdong@qq.com', 'realname': '东东', 'department': boarder, 'is_staff': True,
             'is_superuser': True},
            {'email': 'duoduo@qq.com', 'realname': '多多', 'department': boarder, 'is_staff': True,
             'is_superuser': True},
            {'email': 'zhangsan@qq.com', 'realname': '张三', 'department': developer, 'is_staff': False},
            {'email': 'lisi@qq.com', 'realname': '李四', 'department': operator, 'is_staff': False},
            {'email': 'wangwu@qq.com', 'realname': '王五', 'department': hr, 'is_staff': False},
            {'email': 'zhaoliu@qq.com', 'realname': '赵六', 'department': finance, 'is_staff': False},
            {'email': 'sunqi@qq.com', 'realname': '孙七', 'department': saler, 'is_staff': False},
        ]
        for data in users_data:
            # 使用 update_or_create 避免重复创建
            user, created = OAUser.objects.update_or_create(
                email=data['email'],
                defaults=data
            )
            # 只在新建用户时或密码为空时设置密码
            if created or not user.password:
                user.password = make_password('111111')
                user.save()
        self.stdout.write(self.style.SUCCESS('     用户数据已就绪。'))

        # 获取用户对象
        dongdong = OAUser.objects.get(email="dongdong@qq.com")
        duoduo = OAUser.objects.get(email="duoduo@qq.com")
        zhangsan = OAUser.objects.get(email="zhangsan@qq.com")
        lisi = OAUser.objects.get(email="lisi@qq.com")
        wangwu = OAUser.objects.get(email="wangwu@qq.com")
        zhaoliu = OAUser.objects.get(email="zhaoliu@qq.com")
        sunqi = OAUser.objects.get(email="sunqi@qq.com")

        # --- 步骤 3: 指定部门负责人 ---
        self.stdout.write('  -> 正在指定部门负责人...')

        boarder.leader = '张三'  # 手动输入姓名
        boarder.manager = None
        boarder.save()

        developer.leader = '张三'
        developer.manager = dongdong
        developer.save()

        operator.leader = '李四'
        operator.manager = dongdong
        operator.save()

        saler.leader = '孙七'
        saler.manager = dongdong
        saler.save()

        hr.leader = '王五'
        hr.manager = duoduo
        hr.save()

        finance.leader = '赵六'
        finance.manager = duoduo
        finance.save()

        self.stdout.write(self.style.SUCCESS('     部门负责人已指定。'))
        self.stdout.write(self.style.SUCCESS('--- 所有基础数据填充完毕！ ---'))