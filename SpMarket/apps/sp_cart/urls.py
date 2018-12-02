from django.conf.urls import url

from sp_cart.views import AddCartView, ShopCartView

urlpatterns = [
    url(r'^addCart/$', AddCartView.as_view(), name="addCart"),
    url(r'^$', ShopCartView.as_view(), name="index"),
]
