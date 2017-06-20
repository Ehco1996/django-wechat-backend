from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    context ={
        'bloodmessage':'hei good boy',
    }
    
    return render(request,'hello/index.html',context=context) 


def about(request):
    return render(request,'hello/about.html',context=None)
