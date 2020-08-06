from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import Process
# Create your views here.
@csrf_exempt

def reg(request):
    if request.method == 'POST':
        name=request.POST.get('name')
    print(name)
    return render(request, 'detection/index.html')

def index(request):
    # if request.method == "POST":
    #     uf = UserForm(request.POST,request.FILES)
    #     if uf.is_valid():
    #         print(request.FILES)
    #         #获取表单信息request.FILES是个字典
    #         User = user(headImg=request.FILES['file'])
    #         #保存在服务器
    #         User.save()
    #         return HttpResponse('upload ok!')
    return render(request, 'detection/index.html')