from django.utils.decorators import method_decorator
from django.views import View

from sp_user.helper import verify_login


class BaseVerifyView(View):
    """
        验证视图类, 需要验证登陆的视图类才继承该类
    """
    # 视图类的装饰器
    @method_decorator(verify_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)