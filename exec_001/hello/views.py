from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse('Say hello ')


def about(request):
    return HttpResponse("Say about <a href='/index/'>index</a> ")
