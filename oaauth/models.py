# applications/oaauth/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from shortuuid.django_fields import ShortUUIDField


class UserStatusChoices(models.IntegerChoices):
    ACTIVED = 1, _('已激活')
    UNACTIVE = 2, _('未激活')
    LOCKED = 3, _('已锁定')


class OAUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, realname, email, password, **extra_fields):
        if not realname:
            raise ValueError(_("必须设置真实姓名"))
        if not email:
            raise ValueError(_("必须设置邮箱地址"))
        email = self.normalize_email(email)
        user = self.model(realname=realname, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, realname, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(realname, email, password, **extra_fields)

    def create_superuser(self, realname, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status", UserStatusChoices.ACTIVED)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(realname, email, password, **extra_fields)


class OAUser(AbstractBaseUser, PermissionsMixin):
    """自定义用户模型"""
    uid = ShortUUIDField(_("用户ID"), primary_key=True, length=8, alphabet="1234567890")
    realname = models.CharField(_("真实姓名"), max_length=50)
    email = models.EmailField(_("邮箱"), unique=True)
    telephone = models.CharField(_("手机号"), max_length=20, blank=True, null=True)
    department = models.ForeignKey(
        'OADepartment',  # 正确：使用了字符串
        verbose_name=_("所属部门"),
        on_delete=models.PROTECT, # 建议用 PROTECT，防止误删有员工的部门
        null=True,
        related_name='staffs'
    )
    is_staff = models.BooleanField(_("职员状态"), default=False)
    status = models.IntegerField(_("用户状态"), choices=UserStatusChoices.choices, default=UserStatusChoices.UNACTIVE)
    is_active = models.BooleanField(_("激活状态"), default=True) # is_active=False 用户将无法登录
    date_joined = models.DateTimeField(_("加入日期"), default=timezone.now)

    objects = OAUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["realname"]

    class Meta:
        verbose_name = _("员工")
        verbose_name_plural = _("员工")

    def __str__(self):
        return self.realname

    def get_full_name(self):
        return self.realname

    def get_short_name(self):
        return self.realname


class OADepartment(models.Model):
    """部门模型"""
    name = models.CharField(_("部门名称"), max_length=100, unique=True)
    intro = models.CharField(_("部门简介"), max_length=200, blank=True, null=True)

    leader = models.CharField(_("部门主管(Leader)"), max_length=100, null=True, blank=True)
    manager = models.ForeignKey(
        'OAUser',
        verbose_name=_("上级分管(Manager)"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="manager_of_departments"
    )
    # ============================================

    class Meta:
        verbose_name = _("部门")
        verbose_name_plural = _("部门")

    def __str__(self):
        return self.name