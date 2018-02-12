
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.utils.tool import get_long_random_string, get_short_random_string
from users.models import User


class MoneyCode(models.Model):
    '''充值码'''

    user = models.CharField(
        '用户名',
        max_length=128,
        blank=True,
        null=True,
    )

    code = models.CharField(
        '充值码',
        unique=True,
        blank=True,
        max_length=40,
        editable=False,
        default=get_long_random_string
    )

    number = models.DecimalField(
        '捐赠金额',
        decimal_places=2,
        max_digits=10,
        default=10,
        null=True,
        blank=True,
    )

    create_time = models.DateTimeField(
        '创建时间',
        editable=False,
        auto_now_add=True
    )
    isused = models.BooleanField(
        '是否使用',
        default=False,
    )

    def clean(self):
        # 保证充值码不会重复
        code_length = len(self.code or '')
        if 0 < code_length < 12:
            self.code = '{}{}'.format(
                self.code,
                get_long_random_string()
            )
        else:
            self.code = get_long_random_string()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = '充值码'
        ordering = ('isused',)


class Goods(models.Model):
    '''商品类'''

    info = models.CharField(
        '商品描述',
        max_length=128,
        default='待编辑'
    )

    transfer = models.BigIntegerField(
        '增加的流量(GB)',
        default=settings.GB,
    )

    number = models.DecimalField(
        '金额',
        decimal_places=2,
        max_digits=10,
        default=0,
        null=True,
        blank=True,
    )

    level = models.PositiveIntegerField(
        '商品等级',
        default=0,
    )

    time = models.PositiveIntegerField(
        '设置等级时间(天)',
        default=1,
        validators=[
            MaxValueValidator(365),
            MinValueValidator(1),
        ]
    )

    status = models.IntegerField(
        '商品状态',
        default=1,
        choices=(
            (1, '上架'),
            (0, '下架'),
        )
    )

    def __str__(self):
        return self.info

    def get_transfer_by_GB(self):
        '''增加的流量以GB的形式返回'''
        return '{}'.format(self.transfer / settings.GB)

    def get_days(self):
        '''返回增加的天数'''
        return '{}'.format(self.time)

    class Meta:
        verbose_name_plural = '商品'


class PurchaseHistory(models.Model):
    '''购买记录'''

    info = models.ForeignKey(Goods, on_delete=models.CASCADE)

    user = models.ForeignKey(User, verbose_name='购买者',
                             max_length=128, on_delete=models.CASCADE, related_name='purchase_user')

    number = models.DecimalField(
        '金额',
        decimal_places=2,
        max_digits=10,
        default=0,
        null=True,
        blank=True,
    )

    create_time = models.DateTimeField(
        '购买时间',
        editable=False,
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = '购买记录'
        ordering = ('-create_time',)
