from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class RegisterForm(UserCreationForm):
    '''注册时渲染的表单'''

    username = forms.CharField(label='用户名', help_text='必填。150个字符或者更少。包含字母，数字和仅有的@/./+/-/_符号。',
                               widget=forms.TextInput(
                                   attrs={'class': 'input is-info'})
                               )

    email = forms.CharField(label='邮箱',
                            widget=forms.TextInput(
                                attrs={'class': 'input is-info'})
                            )
    invitecode = forms.CharField(label='邀请码', help_text='邀请码必须填写',
                                 widget=forms.TextInput(
                                     attrs={'class': 'input is-info'})
                                 )
    password1 = forms.CharField(label='密码', help_text='''你的密码不能与其他个人信息太相似。
                                                        你的密码必须包含至少 8 个字符。
                                                        你的密码不能是大家都爱用的常见密码
                                                        你的密码不能全部为数字。''',
                                widget=forms.TextInput(
                                    attrs={'class': 'input is-info'})
                                )
    password2 = forms.CharField(label='重复密码',
                                widget=forms.TextInput(
                                    attrs={'class': 'input is-info'})
                                )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)
