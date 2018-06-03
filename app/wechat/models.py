from io import BytesIO

from django.db import models
from django.core import files
from django.conf import settings

from app import constants


class UserPic(models.Model):
    user_id = models.CharField(max_length=64, blank=True, verbose_name='用户id')
    media_id = models.CharField(max_length=72, verbose_name='图片id', blank=True)
    image = models.ImageField(upload_to='pics/', verbose_name='图片名字')
    create_at = models.DateTimeField(auto_now=True)

    @property
    def img_url(self):
        url = settings.HOST_NAME + self.image.url
        return url

    @classmethod
    def upload_img(cls, user_id, media_id, img_name, img_data):
        f = BytesIO()
        f.write(img_data)
        data = files.File(f)
        pic = cls()
        pic.user_id = user_id
        pic.media_id = media_id
        pic.image.save(img_name, data)
        return pic.img_url

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(UserPic, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = '用户图片'
        ordering = ('-create_at',)


class ReplyRule(models.Model):
    '''自动回复规则model'''

    @classmethod
    def get_all_rules(cls):
        rules = cls.objects.all().values()
        return rules

    @classmethod
    def get_reply(cls, key_word):
        '''
        通过关键字返回对应的信息
        如果没有检索到则返回默认的导航信息
        '''
        reply = cls.objects.filter(key_word__contains=key_word).first()
        if not reply:
            return constants.NAV_BAR
        else:
            return reply.content

    key_word = models.CharField(
        '关键词', max_length=128, blank=False, null=False, unique=True)

    content = models.TextField('回复内容')

    create_at = models.DateTimeField('添加日期', auto_now_add=True)

    def __str__(self):
        return self.key_word

    class Meta:
        ordering = ('-create_at',)
        verbose_name_plural = "自动回复规则"
