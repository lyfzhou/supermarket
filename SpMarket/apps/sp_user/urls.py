from django.conf.urls import url
from sp_user.views import (LoginView,
                           RegisterView,
                           ForgetPassView,
                           MemeberView,
                           InfomationView,
                           send_msg_phone,
                           AddressView,
                           AddressAddView,
                           AddressEditView,
                           delAddress)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),  # 登陆
    url(r'^register/$', RegisterView.as_view(), name="register"),  # 注册
    url(r'^forget/$', ForgetPassView.as_view(), name="forget"),  # 忘记密码
    url(r'^member/$', MemeberView.as_view(), name="member"),  # 个人中心
    url(r'^info/$', InfomationView.as_view(), name="info"),  # 个人资料
    url(r'^sendMsg/$', send_msg_phone, name="sendMsg"),  # 短信地址
    url(r'^address/$', AddressView.as_view(), name="address"),  # 收货地址首页
    url(r'^address/add/$', AddressAddView.as_view(), name="address_add"),  # 收货地址添加
    url(r'^address/edit/(?P<id>\d+)/$', AddressEditView.as_view(), name="address_edit"),  # 收货地址编辑
    url(r'^address/del/$', delAddress, name="address_del"),  # 收货地址删除
]
