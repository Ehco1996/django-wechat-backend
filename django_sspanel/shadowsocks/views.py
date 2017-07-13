from django.shortcuts import render,render_to_response
from django.http import HttpResponse
# Create your views here.
def index(request):
    '''跳转到首页'''
    return render_to_response('sspanel/index.html')

def nodeinfo(request):
    '''跳转到节点信息的页面'''
    
    nodelist = [{'name':'节点一','info':'这个节点是免费节点,点开下方按钮获取节点信息'},
                {'name':'节点二','info':'这个节点是免费节点,点开下方按钮获取节点信息'},
            ]

    context = {
        'nodelists':nodelist,
    }

    return render(request,'sspanel/nodeinfo.html',context=context)