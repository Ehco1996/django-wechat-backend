
import time
import base64
import datetime
from random import choice

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.utils.tool import get_random_string
from users.models import METHOD_CHOICES, PROTOCOL_CHOICES, OBFS_CHOICES


class Node(models.Model):
    '''线路节点'''
    @classmethod
    def get_sub_code(cls, user):
        '''获取该用户的所有节点链接'''
        ss_user = user.ss_user
        sub_code = ''
        node_list = cls.objects.filter(level__lte=user.level, show=1)
        for node in node_list:
            sub_code = sub_code + node.get_ssr_link(ss_user) + "\n"
        return sub_code

    node_id = models.IntegerField('节点id', unique=True,)

    name = models.CharField('名字', max_length=32,)

    server = models.CharField('服务器IP', max_length=128,)

    method = models.CharField(
        '加密类型', default=settings.DEFAULT_METHOD, max_length=32, choices=METHOD_CHOICES,)

    custom_method = models.SmallIntegerField(
        '自定义加密', choices=((0, 0), (1, 1)), default=0,)

    traffic_rate = models.FloatField('流量比例', default=1.0)

    protocol = models.CharField(
        '协议', default=settings.DEFAULT_PROTOCOL, max_length=32, choices=PROTOCOL_CHOICES,)
    protocol_param = models.CharField(
        '协议参数', max_length=128, null=True, blank=True)

    obfs = models.CharField(
        '混淆', default=settings.DEFAULT_OBFS, max_length=32, choices=OBFS_CHOICES,)
    obfs_param = models.CharField(
        '混淆参数', max_length=128, null=True, blank=True)

    info = models.CharField('节点说明', max_length=1024, blank=True, null=True,)

    level = models.PositiveIntegerField(
        '节点等级',
        default=0,
        validators=[
            MaxValueValidator(9),
            MinValueValidator(0),
        ]
    )

    show = models.IntegerField(
        '是否显示',
        choices=(
            (1, '显示'),
            (0, '不显示')),
        default=1,
    )

    group = models.CharField(
        '分组名', max_length=32, default='谜之屋')

    def __str__(self):
        return self.name

    def get_ssr_link(self, ss_user):
        '''返回ssr链接'''
        ssr_password = base64.urlsafe_b64encode(
            bytes(ss_user.password, 'utf8')).decode('ascii')
        ssr_remarks = base64.urlsafe_b64encode(
            bytes(self.name, 'utf8')).decode('ascii')
        ssr_group = base64.urlsafe_b64encode(
            bytes(self.group, 'utf8')).decode('ascii')
        if self.custom_method == 1:
            ssr_code = '{}:{}:{}:{}:{}:{}/?remarks={}&group={}'.format(
                self.server, ss_user.port, ss_user.protocol, ss_user.method, ss_user.obfs, ssr_password, ssr_remarks, ssr_group)
        else:
            ssr_code = '{}:{}:{}:{}:{}:{}/?remarks={}&group={}'.format(
                self.server, ss_user.port, self.protocol, self.method, self.obfs, ssr_password, ssr_remarks, ssr_group)
        ssr_pass = base64.urlsafe_b64encode(
            bytes(ssr_code, 'utf8')).decode('ascii')
        ssr_link = 'ssr://{}'.format(ssr_pass)
        return ssr_link

    def get_ss_link(self, ss_user):
        '''返回ss链接'''
        if self.custom_method == 1:
            ss_code = '{}:{}@{}:{}'.format(
                ss_user.method, ss_user.password, self.server, ss_user.port)
        else:
            ss_code = '{}:{}@{}:{}'.format(
                self.method, ss_user.password, self.server, ss_user.port)
        ss_pass = base64.urlsafe_b64encode(
            bytes(ss_code, 'utf8')).decode('ascii')
        ss_link = 'ss://{}'.format(ss_pass)
        return ss_link

    class Meta:
        ordering = ['id']
        verbose_name_plural = '节点'
        db_table = 'ss_node'
