from django.shortcuts import render,render_to_response
from django.http import HttpResponse

# 导入shadowsocks节点相关文件
from ssserver.models import Node



# Create your views here.
def index(request):
    '''跳转到首页'''
    return render_to_response('sspanel/index.html')

def nodeinfo(request):
    '''跳转到节点信息的页面'''
    
    nodelists = Node.objects.all()

    context = {
        'nodelists':nodelists,
    }

    return render(request,'sspanel/nodeinfo.html',context=context)