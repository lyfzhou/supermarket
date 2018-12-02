from django import forms

from sp_user.helper import set_password
from sp_user.models import SpUser, SpAddress
from django_redis import get_redis_connection

"""
    普通的form
    
    
    modelform

"""


class RegisterModelForm(forms.ModelForm):
    """注册表单, 验证"""
    # 单独添加字段
    password1 = forms.CharField(max_length=16,
                                min_length=6,
                                error_messages={
                                    'required': '密码必填',
                                    'max_length': '密码长度不能大于16个字符',
                                    'min_length': '密码长度必须大于6个字符',
                                }
                                )
    password2 = forms.CharField(error_messages={'required': "确认密码必填"})

    verify_code = forms.CharField(error_messages={"required": "验证码必填!"})

    class Meta:
        model = SpUser
        # 需要验证的字段
        fields = ['phone', ]

        error_messages = {
            "phone": {
                "required": "手机号码必须填写!"
            }
        }

    # 单独清洗(验证)
    def clean_password2(self):
        # 验证两个密码是否一致
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')

        if pwd1 and pwd2 and pwd1 != pwd2:
            # 确认密码错误
            raise forms.ValidationError("两次密码输入不一致!")
        return pwd2

    def clean_phone(self):
        # 验证手机号码是否唯一
        phone = self.cleaned_data.get('phone')
        rs = SpUser.objects.filter(phone=phone).exists()  # 返回bool
        if rs:
            raise forms.ValidationError("手机号码已经被注册")
        return phone

    # 单独验证验证
    def clean_verify_code(self):
        # 获取用户表单提交的
        phone = self.cleaned_data.get("phone")
        verify_code = self.cleaned_data.get('verify_code')
        # 获取redis中的
        r = get_redis_connection("default")
        if phone:
            # 获取 redis中获取的值 是二进制编码,必须解码
            code = r.get(phone)
            code = code.decode("utf-8")
            if code is None:
                raise forms.ValidationError("验证码已经过期或者错误!")
            # 比对
            if verify_code != code:
                raise forms.ValidationError("验证码填写错误!")

            # 最后返回当前字段清洗后的结果
            return verify_code
        else:
            return verify_code


class LoginModelForm(forms.ModelForm):
    """登陆的form表单"""

    class Meta:
        model = SpUser
        fields = ['phone', 'password']

        error_messages = {
            'phone': {
                "required": "手机号码必须填写!"
            },
            'password': {
                "required": "密码必须填写!"
            }
        }

        widgets = {  # 样式
            'phone': forms.TextInput(attrs={"class": "login-name", "placeholder": '请输入手机号'}),
            'password': forms.PasswordInput(attrs={"class": "login-password", "placeholder": '请输入密码'}),
        }

    def clean(self):  # 综合校验
        cleaned_data = self.cleaned_data
        # 获取用手机和密码
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password')
        # 验证手机号码是否存在
        if all([phone, password]):
            # 根据手机号码获取用户
            try:
                user = SpUser.objects.get(phone=phone)
            except SpUser.DoesNotExist:
                raise forms.ValidationError({"phone": "该用户不存在!"})

            # 判断密码是否正确
            if user.password != set_password(password):
                raise forms.ValidationError({"password": "密码填写错误!"})

            # 正确
            # 将用户信息保存到cleaned_data中
            cleaned_data['user'] = user
            return cleaned_data
        else:
            return cleaned_data


class InfoModelForm(forms.ModelForm):
    class Meta:
        model = SpUser
        fields = ['nickname', 'head', 'birth_of_date']

        # error_messages


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = SpAddress
        fields = ['hcity', 'hproper', 'harea', 'detail', 'username', 'phone', 'isDefault']

        error_messages = {
            "harea": {
                "required": "收货地址必填"
            },
            "detail": {
                "required": "详细地址必填"
            },
            "phone": {
                "required": "手机号码必填"
            },
            "username": {
                "required": "收货人姓名必填"
            },
        }

    def clean(self):
        # 验证当前用户的收货地址的数量,如果超过6个就报错
        user_id = self.data.get('user_id')
        count = SpAddress.objects.filter(user_id=user_id, isDelete=False).count()
        if count >= 6:
            raise forms.ValidationError("收货地址数量不能超过6")

        # 默认收货地址只能有一个, 判断当前添加的是否 isDefault==True,
        # 如果是就讲其他的收货地址都设置为False
        isDefault = self.cleaned_data.get("isDefault")
        if isDefault:
            # 如果是就讲其他的收货地址都设置为False
            SpAddress.objects.filter(user_id=user_id).update(isDefault=False)

        return self.cleaned_data


class AddressEditModelForm(forms.ModelForm):
    class Meta:
        model = SpAddress
        fields = ['hcity', 'hproper', 'harea', 'detail', 'username', 'phone', 'isDefault']

        error_messages = {
            "harea": {
                "required": "收货地址必填"
            },
            "detail": {
                "required": "详细地址必填"
            },
            "phone": {
                "required": "手机号码必填"
            },
            "username": {
                "required": "收货人姓名必填"
            },
        }

    def clean(self):
        # 验证当前用户的收货地址的数量,如果超过6个就报错
        user_id = self.data.get('user_id')

        # 默认收货地址只能有一个, 判断当前添加的是否 isDefault==True,
        # 如果是就讲其他的收货地址都设置为False
        isDefault = self.cleaned_data.get("isDefault")
        if isDefault:
            # 如果是就讲其他的收货地址都设置为False
            SpAddress.objects.filter(user_id=user_id).update(isDefault=False)

        return self.cleaned_data
