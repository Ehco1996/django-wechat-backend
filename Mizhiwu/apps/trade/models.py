from django.db import models

from apps.utils.tool import get_long_random_string, get_short_random_string


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
