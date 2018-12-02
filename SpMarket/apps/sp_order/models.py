from django.db import models

from db.base_model import BaseModel


class Transport(BaseModel):
    """
        运输方式
    """
    name = models.CharField(max_length=50, verbose_name="运输方式")
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="运费")

    class Meta:
        db_table = "transport"
        verbose_name = "运输方式管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PayMethod(BaseModel):
    name = models.CharField(verbose_name="支付方式", max_length=50)
    logo = models.ImageField(upload_to="pay/%Y", verbose_name="logo")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "pay_method"
        verbose_name = "支付方式管理"
        verbose_name_plural = verbose_name


class Order(BaseModel):
    order_status = (
        (0, "待付款"),
        (1, "待发货"),
        (2, "已发货"),
        (3, "完成"),
        (4, "已评价"),
        (5, "申请退款"),
        (6, "已退款"),
        (7, "取消订单")
    )
    order_sn = models.CharField(max_length=64, verbose_name="订单编号",unique=True)
    user = models.ForeignKey(to="sp_user.SpUser", verbose_name="用户ID")
    username = models.CharField(max_length=50, verbose_name="收货人姓名")
    phone = models.CharField(max_length=11, verbose_name="收货人电话")
    address = models.CharField(max_length=255, verbose_name="收货人地址")
    status = models.SmallIntegerField(choices=order_status, default=0, verbose_name="订单状态")
    transport = models.CharField(max_length=50, verbose_name="运输方式")
    transport_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="运输方式")
    pay_method = models.ForeignKey(to="PayMethod", verbose_name="支付方式", null=True, blank=True)

    order_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="商品的总价格")
    order_money = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="实际付款金额")

    def __str__(self):
        return self.order_sn

    class Meta:
        db_table = "order"
        verbose_name = "订单管理"
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    """
        订单商品表
        订单ID
        商品SKU ID
        商品数量
        商品价格
    """
    order = models.ForeignKey(to="Order", verbose_name="订单ID")
    goods_sku = models.ForeignKey(to="sp_goods.GoodsSKU", verbose_name="订单商品的SKUID")
    count = models.IntegerField(verbose_name="订单商品的数量")
    price = models.DecimalField(verbose_name="订单商品的价格", max_digits=9, decimal_places=2)

    def __str__(self):
        return self.order.order_sn

    class Meta:
        db_table = "order_goods"
        verbose_name = "订单商品管理"
        verbose_name_plural = verbose_name