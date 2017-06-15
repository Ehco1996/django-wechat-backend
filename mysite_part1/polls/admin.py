from django.contrib import admin
from .models import Question, Choice
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    

    # 自定义每个question里的栏目信息
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields':['pub_date']}),
    ]
    inlines = [ChoiceInline]

    # 自定义每一套question外部浏览的简要信息
    list_display=('question_text','pub_date','was_published_recently')

    # 自定义数据筛选器
    list_filter = ['pub_date']

    # 自定义搜索字段
    search_fields=['question_text']


admin.site.register(Question, QuestionAdmin)
