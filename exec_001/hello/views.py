from django.shortcuts import render, get_object_or_404


from .models import Category, Page


# Create your views here.
def index(request):

    # 按照like的的数量从多到少排序查询
    category_list = Category.objects.order_by('-likes')[:5]
    pages_most_viewed = Page.objects.order_by('-views')[:5]
    
    context = {
        'categories': category_list,
        'pages':pages_most_viewed,
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
