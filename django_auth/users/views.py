from django.shortcuts import render,redirect
from .forms import RegisterForm

# Create your views here.
def register(request):
    '''
    user注册的视图函数
    返回表单的渲染数据
    '''

    # 从get后者post中获取next参数值
    # get请求中，next通过url传递，即 /?next=value
    # post请求中 next通过表单传递，即 <input type='hidden'  name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next',request.GET.get('next',''))
    # 只有当请求为POST的时候，才表示用户提交了注册的信息
    if request.method == 'POST':
        # requst.method 是一个类字典的数据结构，记录了用户提交的注册信息
        # 这里会提交用户名，密码，邮箱
        # 用这些数据，我们来实例化一个用户注册的表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果数据合法，调动表单的save函数，将数据保存到数据库
            form.save()

            # 注册成功，跳转到首页
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 如果不是 POST 表明用户正在访问注册界面，展示一个空的注册表单给用户
        form = RegisterForm()
    

    # 这里我们开始渲染模板
    # 如果用户没有提交数据，我们渲染一个空的表单
    # 如果用户验证的数据不合法，我们渲染一个含有错误信息的表单
    return render(request,'users/register.html',context={'form':form,
                                                         'next':redirect_to,
                                                        })


def index(request):
    return render(request,'index.html')