from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from sp_goods.models import (GoodsSKU,
                             Banner,
                             Activity,
                             ActivityZone,
                             Category)

from django_redis import get_redis_connection

def index(request):
    """首页"""
    # 获取轮播
    banners = Banner.objects.filter(isDelete=False).order_by("-order")

    # 获取活动
    acts = Activity.objects.filter(isDelete=False)

    # 获取特色专区
    act_zones = ActivityZone.objects.filter(is_on_sale=True, isDelete=False).order_by("-order")

    # 渲染数据
    context = {
        "banners": banners,
        "acts": acts,
        "act_zones": act_zones,
    }

    return render(request, "sp_goods/index.html", context)


def category(request, cate_id, order):

    try:
        cate_id = int(cate_id)
        order = int(order)
    except:
        return redirect("sp_goods:首页")

    # 所有的分类 产品经理
    categorys = Category.objects.filter(isDelete=False).order_by("-order")

    # 查询某个分类下的所有商品
    # 默认查询第一个分类
    if cate_id == 0:
        category = categorys.first()
        cate_id = category.pk

    goodsSkus = GoodsSKU.objects.filter(is_on_sale=True, isDelete=False, category_id=cate_id)


    order_rule = ["id", "-sale_num", "-price", "price", "-add_time"]
    try:
        order_one = order_rule[order]
    except:
        order_one = order_rule[0]
        order = 0
    goodsSkus = goodsSkus.order_by(order_one)

    # 对数据进行分页
    pageSize = 10
    paginator = Paginator(goodsSkus,pageSize)

    # 获取某页数据
    p = request.GET.get('p',1)
    try:
        page = paginator.page(p)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page = paginator.page(1)


    # 显示购物车中商品的总数量, 登陆后显示,没有登陆显示为0
    cart_count = 0
    if request.session.get("ID"):
        user_id = request.session.get("ID")
        # 登陆, 从redis中取出购物车中的数据
        r = get_redis_connection("default")
        # 准备键
        cart_key = "cart_key_{}".format(user_id)
        # 取值
        cart_values = r.hvals(cart_key)
        for v in cart_values:
            cart_count += int(v)



    # 渲染数据
    context = {
        "categorys": categorys,
        # "goodsSkus": goodsSkus,
        "goodsSkus": page,
        "cate_id": cate_id,
        "order": order,
        "cart_count": cart_count,
    }
    return render(request, "sp_goods/category.html", context)


def detail(request, id):
    # id goods_sku的id
    # 只需要查询到goodssku就ok
    try:
        goodsSku = GoodsSKU.objects.get(pk=id, is_on_sale=True)
    except GoodsSKU.DoesNotExist:
        # 跳转到首页
        return redirect("sp_goods:首页")

    # 渲染数据到页面
    context = {
        "goodsSku": goodsSku
    }
    return render(request, "sp_goods/detail.html", context)
