from django.db import models

# Create your models here.


class UserPic(models.Model):
    user_id = models.CharField(max_length=64, blank=True, verbose_name='用户id')
    image = models.ImageField(upload_to='pics/', verbose_name='图片名字')
    create_at = models.DateTimeField(auto_now=True)

    @property
    def img_url(self):
        return self.image.url

    class Meta:
        verbose_name_plural = '用户图片'
        ordering = ('-create_at',)
