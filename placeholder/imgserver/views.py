from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from PIL import Image,ImageDraw
from io import BytesIO
from django import forms
import random
from django.core.cache import cache
# Create your views here.


def index(request):
    return render(request, 'imgserver/index.html', context=None)


class ImageForm(forms.Form):
    height =forms.IntegerField(min_value=10,max_value=2000)
    width =forms.IntegerField(min_value=40,max_value=2000)
    def getbgcolor(self):
        return (random.randint(64,255,),random.randint(64,255,),random.randint(64,255,))
    
    def genimg(self,img_format='PNG'):
        width = self.cleaned_data['width']
        height = self.cleaned_data['height']
        # 生成缓存的key
        key = '{}.{}.{}.'.format(width,height,img_format)
        # 从缓存中获得key
        content = cache.get(key)
        
        # 如果不在缓存中
        if content is None:
            # 创建新的图片底层
            image = Image.new('RGB',(width,height))
            # 创建画笔对象
            draw = ImageDraw.Draw(image)
            
            # 填充随机背景色
            bgcolor = self.getbgcolor()
            for x in range(width):
                for y in range(height):
                    draw.point((x,y),bgcolor)
            
            # 获取图片大小的文字
            text = '{}X{}'.format(width,height)

            textwidth,textheight = draw.textsize(text)

            if textheight<height and textwidth<width:
                texttop = (height-textheight)//2
                textleft = (width-textwidth)//2
                draw.text((textleft,texttop),text,fill=(255,255,255))
                content = BytesIO()
                image.save(content,'PNG')
                # 以字节的形式返回
                content.seek(0)
                # 将这个图片加入缓存 缓存周期1小时
                cache.set(key,content,60*60)
        
        return content

def placeholder(request,width,height):
    form = ImageForm({'height':height,'width':width})
    if form.is_valid():
        image = form.genimg()
        return HttpResponse(image,content_type='image/png')
    else:
        return HttpResponseBadRequest('不合法的请求')
        