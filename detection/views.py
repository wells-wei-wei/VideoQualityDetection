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
from .tasks import wrap_ctypes

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

vqd=cdll.LoadLibrary('/home/wells/VideoDetection/libvdq.so')
task_queue = RedisQueue('tasks')
progress_list = RedisQueue('progressList')
result_list = RedisQueue('resultList')

def read_progress_result():
    f = open("data.txt",'a')
    while True:
        progress = progress_list.get_nowait()
        result=result_list.get_nowait()
        if progress:
            print("progress: "+progress.decode())
        if result:
            print("result: "+result.decode())

# def wrap_ctypes(video_id, file_path):
#     print("wrap_ctypes")
#     return vdq.Vqd(video_id, detection_item, file_path)

def test():
    while 1:
        print(os.getpid())
        time.sleep(1)

def detect_video_quality():
    i=1
    while True:
        result = task_queue.get_nowait()
        if not result:
            continue
        wrap_ctypes.delay(i,result.decode())
        i=i+1



detection_progress=Process(target=detect_video_quality)
detection_progress.start()

result_progress=Process(target=read_progress_result)
result_progress.start()

def reg(request):
    if request.method == 'POST':
        name=request.POST.get('name')
    print(name)
    video_files=scan_files(name)
    
    for file in video_files:
        #print(file)
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