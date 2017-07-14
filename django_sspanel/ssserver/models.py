from django.db import models


PLAN_CHOICES = (
    ('free', 'Free'),
)
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
