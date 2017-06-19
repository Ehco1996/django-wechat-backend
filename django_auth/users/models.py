from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    '''
    继承自Django的AbstractUser类
    Username password是必须的， 其字段是可选的
    '''

    nickname = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        pass
    
