import random
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from db.base_view import BaseVerifyView
from sp_user.forms import RegisterModelForm, LoginModelForm, AddressModelForm, AddressEditModelForm
from sp_user.helper import set_password, login, verify_login, send_sms
from sp_user.models import SpUser, SpAddress
import re
from django_redis import get_redis_connection

"""
    开始定义视图:
    1. 函数
    2. 视图类
        a. 定义一个类, 继承 View
        b. 定义方法, 方法名一定要和请求方式名同名(小写 get,post)
        c. 所有的方法都第一个参数和第二个都是固定: self,request
"""


class LoginView(View):
    """登陆"""

    def get(self, request):
        # 创建登陆表单对象
        login_form = LoginModelForm()
        return render(request, "sp_user/login.html", {'form': login_form})

    def post(self, request):
        # 接收数据
        data = request.POST
        # 验证数据
        login_form = LoginModelForm(data)
        if login_form.is_valid():
            # 验证成功后将登陆标识放到session中
            user = login_form.cleaned_data.get('user')
            # 调用登陆的方法,放在helper模块中的
            login(request, user)

            # 判断链接上是否有参数next,如果有就跳转到指定的页面
            next = request.GET.get('next')
            if next:
                return redirect(next)
            else:
                # 跳转到用户中心页面
                return redirect('sp_user:member')
        else:
            return render(request, "sp_user/login.html", {'form': login_form})


@verify_login
def foo(request):
    pass


class RegisterView(View):
    """注册"""

    def get(self, request):
        return render(request, "sp_user/reg.html")

    def post(self, request):
        # 处理
        # 1. 接收
        data = request.POST
        # 2. 处理
        # 验证是否合法
        form = RegisterModelForm(data)
        if form.is_valid():
            # 处理,保存到数据库
            data = form.cleaned_data
            # 密码需要加密
            password = data.get('password2')
            # 调用方法帮助我对密码进行加密
            password = set_password(password)
            # 保存到数据库
            SpUser.objects.create(phone=data.get('phone'), password=password)

            # 成功跳转到登陆页面
            return redirect("sp_user:login")
        else:
            # 传递错误信息到页面
            context = {
                "errors": form.errors,
            }
            # 3. 响应
            return render(request, "sp_user/reg.html", context)


class ForgetPassView(View):
    """找回密码"""

    def get(self, request):
        return render(request, "sp_user/forgetpassword.html")

    def post(self, request):
        pass


class MemeberView(BaseVerifyView):
    """个人中心"""

    def get(self, request):
        context = {
            "phone": request.session.get('phone'),
            "head": request.session.get('head'),
        }
        return render(request, 'sp_user/member.html', context)

    def post(self, request):
        pass

    # # 视图类的装饰器
    # @method_decorator(verify_login)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


class InfomationView(BaseVerifyView):
    """个人资料"""

    def get(self, request):
        # 查询用户的个人信息 进行回显
        # session中保存了用户的id
        user_id = request.session.get("ID")

        # 根据用户id查询用户信息
        user = SpUser.objects.get(pk=user_id)

        # 渲染到页面
        context = {
            "user": user
        }
        return render(request, 'sp_user/infor.html', context)

    def post(self, request):
        # 获取当前用户对象
        user_id = request.session.get("ID")
        user = SpUser.objects.get(pk=user_id)
        user.nickname = request.POST.get("nickname")
        user.gender = request.POST.get("gender")
        # 文件字段
        user.head = request.FILES.get("head")
        user.birth_of_date = request.POST.get("birth_of_date")
        user.save()

        # 重写session
        login(request, user)

        # 跳转
        return redirect("sp_user:member")


def send_msg_phone(request):
    """发生短信的视图函数"""
    if request.method == "POST":
        # 接收到手机号码
        phone = request.POST.get("phone", "")
        # 后端验证手机号码格式是否正确
        # 创建正则对象
        phone_re = re.compile("^1[3-9]\d{9}$")
        # 匹配传入的手机号码
        rs = re.search(phone_re, phone)
        if rs is None:
            # 手机号码格式错误
            return JsonResponse({"err": 1, "errmsg": "手机号码格式错误!"})

        # 生成随机码 随机数字组成
        random_code = "".join([str(random.randint(0, 9)) for _ in range(4)])

        # 保存随机码到redis中
        # 使用redis, 获取redis连接
        r = get_redis_connection("default")
        # 直接开始操作
        r.set(phone, random_code)
        # 设置过期时间
        r.expire(phone, 120)

        # # 发送短信
        # print(random_code)
        #使用阿里发生短信
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\"}" % random_code
        print(send_sms(__business_id, phone, "水酉衣申", "SMS_151577652", params))

        # 成功
        return JsonResponse({"err": 0})
    else:
        # 提示请求方式错误 json 格式
        return JsonResponse({"err": 1, "errmsg": "请求方式错误!"})


class AddressView(BaseVerifyView):
    """
        收货地址列表页
    """

    def get(self, request):
        # 获取收货地址,所有的, 当前用户的
        user_id = request.session.get("ID")
        # 查询
        addresses = SpAddress.objects.filter(user_id=user_id,isDelete=False).order_by("-isDefault")

        # 渲染数据
        context = {
            'addresses': addresses
        }
        return render(request, 'sp_user/gladdress.html', context)

    def post(self, request):
        pass


class AddressAddView(BaseVerifyView):
    """
        收货地址添加页
    """

    def get(self, request):
        return render(request, 'sp_user/address.html')

    def post(self, request):
        # 接收参数
        data = request.POST.dict()
        data['user_id'] = request.session.get("ID")
        # 验证参数
        form = AddressModelForm(data)
        # 处理数据
        if form.is_valid():
            # cleaned_data = form.cleaned_data
            # # cleaned_data['user'] = SpUser.objects.get(pk=request.session.get("ID"))
            # cleaned_data['user_id'] = request.session.get("ID")
            # SpAddress.objects.create(**cleaned_data)
            form.instance.user_id = request.session.get("ID")
            # modelform对象上有个save()方法,直接就能保存数据
            form.save()
            # 返回响应 返回收货地址列表页面
            return redirect("sp_user:address")
        else:
            context = {
                "form": form,
            }
            return render(request, "sp_user/address.html", context)


class AddressEditView(BaseVerifyView):
    """
        收货地址修改页
    """

    def get(self, request, id):
        # 查询当前用户的 当前id的收货地址
        user_id = request.session.get("ID")
        # 查询
        try:
            address = SpAddress.objects.get(user_id=user_id, pk=id)
        except SpAddress.DoesNotExist:
            return redirect("sp_user:address")

        # 渲染到页面
        context = {
            "address": address
        }

        return render(request, 'sp_user/address_edit.html', context)

    def post(self, request, id):
        # 接收数据
        data = request.POST.dict()
        # 验证数据
        user_id = request.session.get("ID")
        data['user_id'] = user_id
        form = AddressEditModelForm(data)
        # 处理数据
        if form.is_valid():
            # 更新 根据主键id
            cleaned_data = form.cleaned_data
            id = data.get('id')
            SpAddress.objects.filter(user_id=user_id, pk=id).update(**cleaned_data)

            # 跳转
            return redirect("sp_user:address")
        else:
            # 返回响应
            context = {
                "form": form,
                "address": data
            }
            return render(request, 'sp_user/address_edit.html', context)


def delAddress(request):
    """删除收货地址"""
    if request.method == "POST":
        # 必须登陆
        user_id = request.session.get('ID')
        id = request.POST.get("id")
        if user_id is None:
            return JsonResponse({"code": 1, "errmsg": "没有登陆!"})
        # 删除的时候最好 用户的id条件加上
        SpAddress.objects.filter(user_id=user_id, pk=id).update(isDelete=True)
        # 返回结果
        return JsonResponse({"code": 0})
    else:
        return JsonResponse({"code": 2,"errmsg":"请求方式错误"})
