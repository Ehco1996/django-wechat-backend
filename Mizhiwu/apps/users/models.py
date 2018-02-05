import base64
import datetime
from random import choice

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MaxValueValidator, MinValueValidator


from apps.utils.tool import get_long_random_string, get_short_random_string


METHOD_CHOICES = (
    ('aes-256-cfb', 'aes-256-cfb'),
    ('aes-128-ctr', 'aes-128-ctr'),
    ('rc4-md5', 'rc4-md5'),
    ('salsa20', 'salsa20'),
    ('chacha20', 'chacha20'),
    ('none', 'none'),
)

PROTOCOL_CHOICES = (
    ('auth_sha1_v4', 'auth_sha1_v4'),
    ('auth_aes128_md5', 'auth_aes128_md5'),
    ('auth_aes128_sha1', 'auth_aes128_sha1'),
    ('auth_chain_a', 'auth_chain_a'),
    ('origin', 'origin'),
)


OBFS_CHOICES = (
    ('plain', 'plain'),
    ('http_simple', 'http_simple'),
    ('http_simple_compatible', 'http_simple_compatible'),
    ('http_post', 'http_post'),
    ('tls1.2_ticket_auth', 'tls1.2_ticket_auth'),
)

STATUS_CHOICES = (
    ('好用', '好用'),
    ('维护', '维护'),
    ('坏了', '坏了'),
)


class User(AbstractUser):
    '''SS账户模型'''

    @classmethod
    def proUser(cls):
        '''付费用户数量'''
        return len(cls.objects.filter(level__gt=0))

    @classmethod
    def userNum(cls):
        '''用户总数'''
        return len(cls.objects.all())

    @classmethod
    def todayRegister(cls):
        '''今日注册的用户'''
        # 获取今天凌晨的时间
        today = datetime.datetime.combine(
            datetime.date.today(), datetime.time.min)
        return cls.objects.filter(date_joined__gt=today)

    @classmethod
    def userTodyChecked(cls):
        '''今日签到人数'''
        return len([o for o in cls.objects.all() if o.get_check_in()])

    @classmethod
    def userNeverChecked(cls):
        '''从未签到过人数'''
        return len([o for o in cls.objects.all() if o.last_check_in_time.year == 1970])

    @classmethod
    def userNeverUsed(cls):
        '''从未使用过的人数'''
        return len([o for o in cls.objects.all() if o.last_use_time == 0])

    @classmethod
    def randomPord(cls):
        '''随机端口'''
        users = cls.objects.all()
        port_list = []
        for user in users:
            port_list.append(user.port)
        all_ports = [i for i in range(1025, max(port_list) + 1)]
        try:
            return choice(list(set(all_ports).difference(set(port_list))))
        except:
            return max(port_list) + 1

    balance = models.DecimalField(
        '余额',
        decimal_places=2,
        max_digits=10,
        default=0,
        editable=True,
        null=True,
        blank=True,
    )

    invitecode_num = models.PositiveIntegerField(
        '邀请码数量',
        default=settings.INVITE_NUM
    )

    invite_user = models.ForeignKey(
        'self', on_delete=models.SET_NULL, related_name='inviter', verbose_name='邀请人', blank=True, null=True)

    # 最高等级限制为9级，和节点等级绑定
    level = models.PositiveIntegerField(
        '等级',
        default=0,
        validators=[
            MaxValueValidator(9),
            MinValueValidator(0),
        ]
    )

    level_expire_time = models.DateTimeField(
        '等级有效期',
        default=timezone.now,
        help_text='等级有效期',
    )

    theme = models.CharField(
        '主题',
        max_length=10,
        default='default',
    )

    last_check_in_time = models.DateTimeField(
        '最后签到时间',
        null=True,
        # 默认设置为时间戳开始的那天
        default=datetime.datetime.fromtimestamp(0),
        editable=False,
    )
    # shadowsocks passwprd
    sspasswd = models.CharField(
        'Shadowsocks密码',
        max_length=32,
        # 当密码少于6位时报错
        validators=[validators.MinLengthValidator(6), ],
        default=get_short_random_string,
        db_column='passwd',
    )
    port = models.IntegerField(
        '端口',
        db_column='port',
        unique=True,
        default=settings.START_PORT
    )

    last_use_time = models.IntegerField(
        '最后使用时间',
        default=0,
        editable=False,
        help_text='时间戳',
        db_column='t'
    )
    upload_traffic = models.BigIntegerField(
        '上传流量',
        default=0,
        db_column='u'
    )
    download_traffic = models.BigIntegerField(
        '下载流量',
        default=0,
        db_column='d'
    )
    transfer_enable = models.BigIntegerField(
        '总流量',
        default=settings.DEFAULT_TRAFFIC,
        db_column='transfer_enable'
    )
    switch = models.BooleanField(
        '保留字段switch',
        default=True,
        db_column='switch',
    )
    enable = models.BooleanField(
        '开启与否',
        default=True,
        db_column='enable',
    )
    method = models.CharField(
        '加密类型', default=settings.DEFAULT_METHOD, max_length=32, choices=METHOD_CHOICES,)

    protocol = models.CharField(
        '协议', default=settings.DEFAULT_PROTOCOL, max_length=32, choices=PROTOCOL_CHOICES,)
    protocol_param = models.CharField(
        '协议参数', max_length=128, null=True, blank=True)

    obfs = models.CharField(
        '混淆', default=settings.DEFAULT_OBFS, max_length=32, choices=OBFS_CHOICES,)
    obfs_param = models.CharField(
        '混淆参数', max_length=128, null=True, blank=True)

    def __str__(self):
        return self.username

    def get_last_use_time(self):
        '''上一次的使用到时间'''
        return timezone.datetime.fromtimestamp(self.last_use_time)

    def get_traffic(self):
        '''用户使用的总流量GB '''
        return '{:.2f}'.format((self.download_traffic + self.upload_traffic) / settings.GB)

    def get_transfer(self):
        '''用户的总流量 GB'''
        return '{:.2f}'.format(self.transfer_enable / settings.GB)

    def get_unused_traffic(self):
        '''用户的剩余流量'''
        return '{:.2f}'.format((self.transfer_enable - self.upload_traffic - self.download_traffic) / settings.GB)

    def get_used_percentage(self):
        '''返回用户的为使用流量百分比'''
        try:
            return '{:.2f}'.format((self.download_traffic + self.upload_traffic) / self.transfer_enable * 100)
        except ZeroDivisionError:
            return '100'

    def get_check_in(self):
        '''当天是否签到'''
        # 获取当天日期
        check_day = self.last_check_in_time.day
        now_day = datetime.datetime.now().day
        return check_day == now_day

    def clean(self):
        '''保证端口在1024<50000之间'''
        if self.port:
            if not 1024 < self.port < 50000:
                raise ValidationError('端口必须在1024和50000之间')

    def get_expire_time(self):
        '''返回等级到期时间'''
        return self.level_expire_time

    def get_sub_link(self):
        '''生成该用户的订阅地址'''
        # 订阅地址
        token = base64.b64encode(
            bytes(self.username, 'utf-8')).decode('ascii')
        sub_link = settings.HOST + 'server/subscribe/' + token + '/'
        return sub_link

    class Meta(AbstractUser.Meta):
        verbose_name = '用户'
        db_table = 'user'


class InviteCode(models.Model):
    '''邀请码'''

    code = models.CharField(
        '邀请码',
        primary_key=True,
        blank=True,
        max_length=40,
        default=get_long_random_string
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='创建者', related_name='code_owner',help_text='用户ID')

    isused = models.BooleanField(
        '是否使用',
        default=False,
    )
    code_type = models.IntegerField(
        '类型',
        choices=((1, '公开'), (0, '不公开')),
        default=1,
    )
    time_created = models.DateTimeField(
        '创建时间',
        editable=False,
        auto_now_add=True
    )

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name_plural = '邀请码'
        ordering = ('isused', '-time_created',)
        db_table = 'invitecode'
