from django.db import models


class BaseModel(models.Model):
    """基础模型类"""
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        # 设置抽象的类
        abstract = True