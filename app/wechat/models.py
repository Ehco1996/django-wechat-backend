from io import BytesIO

from django.db import models
from django.core import files
from django.conf import settings


class UserPic(models.Model):
    user_id = models.CharField(max_length=64, blank=True, verbose_name='用户id')
    image = models.ImageField(upload_to='pics/', verbose_name='图片名字')
    create_at = models.DateTimeField(auto_now=True)

    @property
    def img_url(self):
        url = settings.HOST_NAME + self.image.url
        return url

    @classmethod
    def upload_img(cls, user_id, img_name, img_data):
        f = BytesIO()
        f.write(img_data)
        data = files.File(f)
        pic = cls()
        pic.user_id = user_id
        pic.image.save(img_name, data)
        return pic.img_url

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(UserPic, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = '用户图片'
        ordering = ('-create_at',)
