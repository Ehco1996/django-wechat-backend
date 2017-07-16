from django.db import models
from django.contrib.auth.models import AbstractUser


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
        blank=True,
        max_length=40,
    )
    
    
    
    
    def __str__(self):
        return self.username

    
    def set_password(self,raw_password):
        '''将password改变成明文，便于后台管理'''
        self.password = raw_password
    
    def check_password(self,raw_password):
        return self.password==raw_password
    
    
    
    class Meta(AbstractUser.Meta):
        verbose_name='用户'

    