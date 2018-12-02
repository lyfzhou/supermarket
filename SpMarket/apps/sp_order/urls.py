from django.conf.urls import url

from sp_order.views import ConfirmOrder, OrderShow, pay, success

urlpatterns = [
    url(r'^confirm/$', ConfirmOrder.as_view(), name="确认订单"),
    url(r'^show/$', OrderShow.as_view(), name="确认支付"),
    url(r'^pay/$', pay, name="发起支付"),
    url(r'^success/$', success, name="支付成功"),
]
