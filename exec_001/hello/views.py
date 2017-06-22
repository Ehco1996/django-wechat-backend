from django.shortcuts import render, get_object_or_404


from .models import Category, Page
from .forms import CategoryForm, PageForm

# Create your views here.


def index(request):

    # 按照like的的数量从多到少排序查询
    category_list = Category.objects.order_by('-likes')[:5]
    pages_most_viewed = Page.objects.order_by('-views')[:5]

    context = {
        'categories': category_list,
        'pages': pages_most_viewed,
    }

    return render(request, 'hello/index.html', context=context)


def about(request):
    return render(request, 'hello/about.html', context=None)


def category(request, category_name):
    # 从url里补货的类别名字
    category = get_object_or_404(Category, name=category_name)
    try:
        pages = Page.objects.filter(category=category)

        context = {
            'category_name': category_name,
            'pages': pages,
            'category': category,
        }
    except:
        # 没有找到相对于的分类的情况下
        context = {'category_name': category_name}

    return render(request, 'hello/category.html', context=context)


def add_category(request):

    # 判断是否是一个post请求
    if request.method == 'POST':
        # 通过POST数据来构造一个有数据的form
        form = CategoryForm(request.POST)

        # 判断数据是否合法：
        if form.is_valid():
           # 将数据保存到数据库中
            form.save(commit=True)
            # 调用index函数，让用户返回主页
            return index(request)
        else:
            # 如果数据不合法，我们就将错误信息渲染出去
            print(form.errors)
    else:
        # 如果不是一个post请求，
        # 那说明用户正在访问填写表单的页面
        # 我们就渲染出一个空的表单来给用户填写
        form = CategoryForm()

    return render(request, 'hello/add_category.html', context={'form': form, })


def add_page(request,category_name):

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            
            # 我们先保存数据，但是不向数据库里提交数据
            # 这是因为我们还需要手动补全分类的信息
            page = form.save(commit=False)
            # 我们从url中捕获想要添加的分类名
            cat = Category.objects.get(name=category_name)
            page.category = cat

            # 接着我们需要补全views
            page.views=0

            
            # 最后，我们将数据传入数据库
            page.save()
            return index(request)
        else:
            print(form.errors)
    else:
        form = PageForm()

    return render(request, 'hello/add_page.html', context={'form': form,
                                                           'category_name':category_name, 
                                                            })
