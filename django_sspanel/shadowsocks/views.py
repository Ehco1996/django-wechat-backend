from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
# 导入shadowsocks节点相关文件
from .models import Node, InviteCode,User
from .forms import RegisterForm,LoginForm

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

    context = {'codelist': codelist, }

    return render(request, 'sspanel/invite.html', context=context)


def gen_invite_code(request, Num=10):
    '''生成指定数量的邀请码，默认为十个'''
    for i in range(int(Num)):
        code = InviteCode()
        code.save()
    return HttpResponse('邀请码添加成功')


def pass_invitecode(request, invitecode):
    '''提供点击邀请码连接之后自动填写邀请码'''
    form = RegisterForm(initial={'invitecode':invitecode})
    return render(request, 'sspanel/register.html', {'form': form})

def nodeinfo(request):
    '''跳转到节点信息的页面'''

    nodelists = Node.objects.all()

    context = {
        'nodelists': nodelists,
    }

    return render(request, 'sspanel/nodeinfo.html', context=context)



def register(request):
    '''用户注册时的函数'''
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            # 获取用户填写的邀请码
            code = request.POST.get('invitecode')
            # 数据库查询邀请码
            code_query = InviteCode.objects.filter(code=code)
            # 判断邀请码是否存在并返回信息
            if len(code_query) == 0:
                registerinfo = {
                    'title': '邀请码失效',
                    'subtitle': '请重新获取邀请码',
                    'status': 'error',
                }
                context = {
                    'registerinfo': registerinfo,
                    'form': form,
                }
                return render(request, 'sspanel/register.html', context=context)

            else:
                registerinfo = {
                    'title': '注册成功！',
                    'subtitle': '请登录使用吧！',
                    'status': 'success',
                }
                context = {
                    'registerinfo': registerinfo
                }
                form.save()
                code_query.delete()
                return render(request, 'sspanel/index.html', context=context)

    else:
        form = RegisterForm()

    return render(request, 'sspanel/register.html', {'form': form})

def Login(request):
    '''用户登录函数'''
    if request.method=='POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            # 获取表单用户名和密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 和数据库信息进行比较
            user = User.objects.filter(username=username,password=password)

            if user:
                registerinfo = {
                    'title': '登录成功！',
                    'subtitle': '自动跳转到用户中心',
                    'status': 'success',
                }
                context = {
                    'registerinfo': registerinfo
                }
                return render(request, 'sspanel/userinfo.html', context=context)
            else:
                form = LoginForm()
                registerinfo = {
                    'title': '登录失败！',
                    'subtitle': '请重新填写信息！',
                    'status': 'error',
                }
                context = {
                    'registerinfo': registerinfo,
                    'form':form,

                }
                return render(request, 'sspanel/login.html', context=context)
    else:
        form = LoginForm()
        return render(request, 'sspanel/login.html', {'form': form})
    

def Userinfo(request):
    '''用户中心'''
    render_to_response(request,'sspanel/userinfo.html')