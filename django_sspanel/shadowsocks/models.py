from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password ,check_password

# 自己写的小脚本 用于生成邀请码
from .tools import get_long_random_string, get_short_random_string

METHOD_CHOICES = (
    ('aes-256-cfb', 'aes-256-cfb'),
    ('rc4-md5', 'rc4-md5'),
    ('salsa20', 'salsa20'),
    ('aes-128-ctr', 'aes-128-ctr'),
)
STATUS_CHOICES = (
    ('ok', '好用'),
    ('slow', '不好用'),
    ('fail', '坏了'),
)

# Create your models here.
class User(AbstractUser):
    '''SS账户模型'''

    balance = models.DecimalField(
        '余额',
        decimal_places=2,
        max_digits=10,
        default=0,
        editable=False,
        null=True,
        blank=True,
    )

    invitecode = models.CharField(
        '邀请码',
        max_length=40,
    )

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        '''使用md5加密算法'''
        raw_password= make_password(raw_password,'MD5PasswordHasher')
        self.password = raw_password

    def check_password(self, raw_password):

        return check_password(raw_password,make_password(raw_password,'MD5PasswordHasher'))

    class Meta(AbstractUser.Meta):
        verbose_name = '用户'



class Node(models.Model):
    '''线路节点'''

    name = models.CharField('名字', max_length=32,)

    server = models.CharField('服务器IP', max_length=128,)

    menthod = models.CharField(
        '加密类型', default='aes-256-cfb', max_length=32, choices=METHOD_CHOICES,)

    info = models.CharField('节点说明', max_length=1024, blank=True, null=True,)

    status = models.CharField(
        '状态', max_length=32, default='ok', choices=STATUS_CHOICES,)

    node_id = models.IntegerField('节点id', primary_key=True,)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['node_id']
        verbose_name_plural = '节点'


class InviteCode(models.Model):
    '''邀请码'''

    code = models.CharField(
        '邀请码',
        primary_key=True,
        blank=True,
        max_length=40,
        default=get_long_random_string
    )

    time_created = models.DateTimeField(
        '创建时间',
        editable=False,
        auto_now_add=True
    )

    def clean(self):
        # 保证邀请码不会重复
        code_length = len(self.code or '')
        if 0 < code_length <16:
            self.code = '{}{}'.format(
                    self.code,
                    get_long_random_string()
            )
        else:
            self.code = None
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        
        # 重写save方法，在包存前执行我们写的clean方法
        self.clean()
        return super(InviteCode, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name_plural = '邀请码'
        ordering = ('-time_created',)