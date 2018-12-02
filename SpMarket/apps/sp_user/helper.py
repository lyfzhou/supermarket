import hashlib
from django.conf import settings
from django.shortcuts import redirect
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from django.conf import settings

def set_password(password):
    # 加密方法
    # 新的加密字符串
    new_password = "{}{}".format(password, settings.SECRET_KEY)
    h = hashlib.md5(new_password.encode('utf-8'))
    return h.hexdigest()


def login(request, user):
    # 登陆保存session的方法
    # 将用户id和手机号码,保存到session中
    request.session['ID'] = user.pk
    request.session['phone'] = user.phone
    request.session['head'] = user.head
    request.session.set_expiry(0)



def verify_login(func):
    """验证登陆装饰器"""
    def check_loign(request, *args, **kwargs):
        if request.session.get("ID") is None:
            # 没有登录跳转到登陆页面
            return redirect('sp_user:login')
        else:
            return func(request, *args, **kwargs)
    return check_loign


# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)
    # TODO 业务处理
    return smsResponse