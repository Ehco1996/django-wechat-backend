from django.db import models
from django.utils import timezone

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
        return self.pub_date >= timezone.now() - timezone.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
