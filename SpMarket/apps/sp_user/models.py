from django.db import models

from db.base_model import BaseModel
from django.core.validators import RegexValidator


class SpUser(BaseModel):
    """
        用户表
    """
    sex_choices = (
        (1, "男"),
        (2, "女"),
    )
    phone = models.CharField(max_length=11,
                             verbose_name="手机号码",
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
                             ])
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name="昵称")
    password = models.CharField(max_length=32, verbose_name="密码")
    gender = models.SmallIntegerField(choices=sex_choices, default=1, verbose_name="性别")
    school_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="学校")
    hometown = models.CharField(max_length=50, null=True, blank=True, verbose_name="家乡")
    birth_of_date = models.DateField(null=True, blank=True, verbose_name="出生日期")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="详细位置")
    # 设置头像字段
    head = models.ImageField(upload_to="head/%Y%m", default="head/memtx.png", verbose_name="用户头像")

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "sp_user"
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name


class SpAddress(BaseModel):
    hcity = models.CharField(max_length=50, null=True, blank=True, verbose_name="省")
    hproper = models.CharField(max_length=50, null=True, blank=True, verbose_name="市")
    harea = models.CharField(max_length=50, verbose_name="区")
    detail = models.CharField(max_length=255, verbose_name="详细地址")
    username = models.CharField(max_length=100, verbose_name="收货人姓名")
    phone = models.CharField(max_length=11,
                             verbose_name="收货人手机号",
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误"),
                             ],
                             )
    user = models.ForeignKey(to="sp_user.SpUser", verbose_name="所属用户")
    isDefault = models.BooleanField(default=False, verbose_name="是否为默认地址")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "sp_address"
        verbose_name = "收货地址管理"
        verbose_name_plural = verbose_name
