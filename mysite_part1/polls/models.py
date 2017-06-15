from django.db import models
from django.utils import timezone
import datetime
# Create your models here.


class Question(models.Model):
    '''
    字段名：
    database will use it as the column name
    '''

    question_text = models.CharField(max_length=200)
    # 这里的第一个参数是给该字段起了一个人类更加容易辨识的名字
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        # 表明这问题的发布时间一定在现在之前
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Publishen recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
