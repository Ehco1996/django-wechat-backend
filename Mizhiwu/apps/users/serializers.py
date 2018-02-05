from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import InviteCode

# 获取当前用户模型
User = get_user_model()


class UserInfoSerializer(serializers.ModelSerializer):
    '''
    用户基本信息序列化
    '''
    # 外键关系模型
    invite_user = serializers.ReadOnlyField(source='invite_user.username')

    class Meta:
        model = User
        fields = ('id','username', 'email', 'invite_user', 'balance',
                  'level', 'level_expire_time', 'theme')


class UserSsConfigSerializer(serializers.ModelSerializer):
    '''
    用户shadowsocks配置序列化
    '''

    class Meta:
        model = User
        fields = ('username', 'port', 'method', 'sspasswd', 'protocol',
                  'protocol_param', 'obfs', 'obfs_param')


class UserSsUsageSerializer(serializers.ModelSerializer):
    '''
    用户shadowsocks使用情况序列化
    '''

    class Meta:
        model = User
        fields = ('username', 'enable', 'last_use_time', 'upload_traffic', 'download_traffic',
                  'transfer_enable')


class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册序列化
    '''
    code = serializers.CharField(required=True, write_only=True, label="邀请码",
                                 error_messages={
                                     "blank": "请输入邀请码",
                                     "required": "请输入邀请码",
                                     "max_length": "邀请码错误",
                                     "min_length": "邀请码错误"
                                 },
                                 help_text="邀请码")

    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    email = serializers.EmailField(label='邮箱', help_text='邮箱', required=True, allow_blank=False, validators=[
                                   UniqueValidator(queryset=User.objects.all(), message="邮箱已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate_code(self, code):
        '''
        验证邀请码
        '''
        code_query = InviteCode.objects.filter(code=code)
        if len(code_query) < 1:
            raise serializers.ValidationError('邀请码不正确')
        else:
            code = code_query[0]
            if code.isused == True:
                raise serializers.ValidationError('邀请码已经被使用了！')
        return code

    class Meta:
        model = User
        fields = ("username", "email", "password", "code")


class InviteCodeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = InviteCode
        fields = '__all__'


class InviteCodeCreateSerializer(serializers.ModelSerializer):
    def validate_owner(self, owner):
        '''
        验证可生成邀请码的数量
        '''
        code_query = InviteCode.objects.filter(owner=owner)
        user = User.objects.get(username=owner)
        if user.is_staff == True:
            return owner
        if len(code_query) > user.invitecode_num:
            raise serializers.ValidationError('已到当前用户可以生成邀请码的最大数量')
        return owner

    class Meta:
        model = InviteCode
        fields = ('owner',)
