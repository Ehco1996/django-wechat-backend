# 导入django内置模块
from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.six import BytesIO
from django.utils import timezone


# 导入shadowsocks节点相关文件
from .models import Node, InviteCode, User
from .forms import RegisterForm, LoginForm

# 导入ssservermodel
from ssserver.models import SSUser

# 导入第三方模块
import qrcode
import base64
import datetime
from random import randint
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
    form = RegisterForm(initial={'invitecode': invitecode})
    return render(request, 'sspanel/register.html', {'form': form})


def nodeinfo(request):
    '''跳转到节点信息的页面'''

    nodelists = Node.objects.all()
    ss_user = request.user.ss_user
    context = {
        'nodelists': nodelists,
        'ss_user':ss_user,
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
                # 删除使用过的邀请码
                code_query.delete()
                # 将user和ssuser关联
                user = User.objects.get(username=request.POST.get('username'))
                max_port_user = SSUser.objects.order_by('-port').first()
                port = max_port_user.port+randint(2,3)
                ss_user = SSUser.objects.create(user=user,port=port)
                return render(request, 'sspanel/index.html', context=context)

    else:
        form = RegisterForm()

    return render(request, 'sspanel/register.html', {'form': form})


def Login_view(request):
    '''用户登录函数'''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 获取表单用户名和密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 和数据库信息进行比较
            #user = User.objects.filter(username=username,password=password)
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
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
                    'form': form,

                }
                return render(request, 'sspanel/login.html', context=context)
    else:
        form = LoginForm()
        return render(request, 'sspanel/login.html', {'form': form})


def Logout_view(request):
    '''用户登出函数'''
    logout(request)
    registerinfo = {
        'title': '注销成功！',
        'subtitle': '欢迎下次再来!！',
                    'status': 'success',
    }
    context = {
        'registerinfo': registerinfo,
    }

    return render(request, 'sspanel/index.html', context=context)


@login_required
def userinfo(request):
    '''用户中心'''

    ss_user = request.user.ss_user
    context = {
            'ss_user':ss_user,
    }

    return render(request, 'sspanel/userinfo.html',context=context)

@login_required
def checkin(request):
    '''用户签到'''
    ss_user = request.user.ss_user
    if timezone.now() - datetime.timedelta(days=1) > ss_user.last_check_in_time:
        # 距离上次签到时间大于一天 增加200m流量
        ss_user.transfer_enable += int(200*1024*1024)    
        ss_user.last_check_in_time = timezone.now()
        ss_user.save()
        registerinfo = {
        'title': '签到成功！',
        'subtitle': '获得200m流量',
                    'status': 'success',}
    else:
        registerinfo = {
        'title': '签到失败！',
        'subtitle': '距离上次签到不足一天',
                    'status': 'error',}
    
    context = {
        'registerinfo': registerinfo,
        'ss_user':ss_user,
    }
    return render(request,'sspanel/userinfo.html',context=context)

@login_required
def get_ss_qrcode(request,node_id):
    '''返回节点配置信息的二维码'''
    # 获取用户对象
    ss_user = request.user.ss_user
    # 获取节点对象
    node = Node.objects.get(node_id=node_id)
    
    code = '{}:{}@{}:{}'.format(node.method,ss_user.password,node.server,ss_user.port)
    # 将信息编码
    qrpass = base64.b64encode(bytes(code,'utf8')).decode('ascii')
    img = qrcode.make('ss://{}'.format(qrpass))
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    # 构造图片reponse
    response = HttpResponse(image_stream, content_type="image/png")
    
    return response




from random import choice
# Create your views here.

