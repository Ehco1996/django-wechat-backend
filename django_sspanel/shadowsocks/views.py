from django.shortcuts import render,render_to_response
from django.http import HttpResponse
# Create your views here.
def index(request):
    '''跳转到首页'''
    return render_to_response('base.html')