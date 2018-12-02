from django.contrib import admin
from sp_goods.models import (Category,
                             Unit,
                             GoodsSPU,
                             GoodsSKU,
                             Gallery,
                             ActivityZone,
                             ActivityZoneGoods,
                             Banner,
                             Activity,
                             )

"""
注册方式:
admin.site.register(模型类)

装饰器形式注册
@admin.register(模型类)
class XxxAdmin(admin.ModelAdmin):
    # 自定义后显示的类
"""

# admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 自定义后台
    list_display = ['id','cate_name','brief','order','update_time']
    list_display_links = ['id','cate_name','brief']


admin.site.register(Unit)

admin.site.register(GoodsSPU)


# 商品sku
class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 2

@admin.register(GoodsSKU)
class GoodsSkuAdmin(admin.ModelAdmin):
    list_display = ["id",'sku_name','price','unit','stock','sale_num','show_logo','is_on_sale','category']
    list_display_links = ["id",'sku_name','price']


    search_fields = ['sku_name','price','sale_num']
    inlines = [
        GalleryInline,
    ]


# 首页管理
admin.site.register(Banner)
admin.site.register(Activity)


class ActivityZoneGoodsInline(admin.TabularInline):
    model = ActivityZoneGoods
    extra = 2


@admin.register(ActivityZone)
class ActivityZoneAdmin(admin.ModelAdmin):
    inlines = [
        ActivityZoneGoodsInline
    ]
# admin.site.register(ActivityZone)
# admin.site.register(ActivityZoneGoods)






