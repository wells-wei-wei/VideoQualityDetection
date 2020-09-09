from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import Process
from redis_queue import RedisQueue
import os
import time
from ctypes import *
from multiprocessing import Pool, Process
from detection.models import Task
from django.utils import timezone

# Create your views here.
# @csrf_exempt

def scan_files(file_path):
    video_format=['mp4', 'avi', 'MP4', 'AVI']
    video_files=[]
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file[-3:] in video_format:
                video_files.append(os.path.join(root,file))

    return video_files

task_queue = RedisQueue('tasks')

def test():
    while 1:
        print(os.getpid())
        time.sleep(1)

def reg(request):
    if request.method == 'POST':
        name=request.POST.get('name')
    video_files=scan_files(name)
    
    new_task = Task(task_name=name, start_time=timezone.now(), finish_time=timezone.now())
    new_task.save()

    for file in video_files:
        #print(file)
        file=str(new_task.id)+"-"+file
        # print(file)
        task_queue.put(file)
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