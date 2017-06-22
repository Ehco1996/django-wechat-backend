from django import forms
from .models import Page,Category

# 所有的form都必须继承自django内置的form类，这样才能将form自动选染成html widgets
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,help_text='请输入类别名字')
    # 这里我们将views和likes的字段初始化为0，并且隐藏起来，
    # 这样form在向model提交数据的时候，就不会出现字段为空的错误
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    
    # 一个内置的元类，向form提供了额外需要的信息
    class Meta:
        # 这里建立了form和model的联系
        model = Category
        fields = ('name',) 

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,help_text='请输入文章名')
    url = forms.URLField(max_length=128,help_text='请输入文章的链接')
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    def clean(self):
        '''
        方便的补全url
        '''
        # 从父类得到cleaned_data
        cleaned_data = super(PageForm,self).clean()
        
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data

    class Meta:
        model = Page

        # 这里规定了我们的form里显示哪些字段
        # 这样我们就不用显示model里的所有字段
        # 比如null的字段，
        # 在这个例子中，我们省略了外键 category的字段
        fields = ('title','url','views')    
    
    