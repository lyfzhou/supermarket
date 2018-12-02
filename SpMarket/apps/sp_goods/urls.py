from django.conf.urls import url

from sp_goods.views import index, category, detail

urlpatterns = [
    url(r'^$', index, name="首页"),
    url(r'^category/(?P<cate_id>\d+)/(?P<order>\d)/$', category, name="分类"),
    url(r'^(?P<id>\d+).html$', detail, name="详情"),
]
