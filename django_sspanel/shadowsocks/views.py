from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse

# 导入shadowsocks节点相关文件
from ssserver.models import Node,InviteCode
from .forms import RegisterForm



# Create your views here.
def index(request):
    '''跳转到首页'''
    return render_to_response('sspanel/index.html')


def sshelp(request):
    '''跳转到帮助界面'''
    return render_to_response('sspanel/help.html')
    
def ssclient(request):
    '''跳转到客户端界面'''
    return render_to_response('sspanel/client.html')
    


def ssinvite(request):
    '''跳转到邀请码界面'''
    codelist = InviteCode.objects.all()
    
    context = {'codelist':codelist,}

    return render(request,'sspanel/invite.html',context=context)

def gen_invite_code(request,Num=10):
    '''生成指定数量的邀请码，默认为十个'''
    for i in range(int(Num)):
        code = InviteCode()
        code.save()
    return HttpResponse('邀请码添加成功')


def register(request):
    '''用户注册时的函数'''
    if request.method== 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')
    else:
        form = RegisterForm()
    
    return render(request,'sspanel/register.html',{'form':form})


def nodeinfo(request):
    '''跳转到节点信息的页面'''
    
    nodelists = Node.objects.all()

    context = {
        'nodelists':nodelists,
    }

    return render(request,'sspanel/nodeinfo.html',context=context)