from __future__ import absolute_import, unicode_literals
from celery import Celery
from ctypes import *
import time
from redis_queue import RedisQueue
from celery import shared_task
from multiprocessing import Pool, Process
import os

vqd=cdll.LoadLibrary('/home/wells/VideoDetection/libvdq.so')
celery_app = Celery('a', broker='redis://localhost:6379/0')
task_queue = RedisQueue('tasks')
progress_list = RedisQueue('progressList')
result_list = RedisQueue('resultList')

@shared_task
def wrap_ctypes(video_id, file_path):
    file_path=file_path.encode()
    print("使用celery")
    five = c_int * 16
    detection_item = five(0,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0)
    return vqd.Vqd(video_id, detection_item, file_path)

@shared_task
def test(n):
    print(n)

def detect_video_quality():
    i=1
    while True:
        result = task_queue.get_nowait()
        if not result:
            continue
        wrap_ctypes.delay(i,result.decode())
        i=i+1

def read_progress_result():
    # f = open("data.txt",'a')
    while True:
        progress = progress_list.get_nowait()
        result=result_list.get_nowait()
        if progress:
            #print(os.getpid())
            print("progress: "+progress.decode())
            #f.write(str(os.getpid()))
        if result:
            #print(os.getpid())
            print("result: "+result.decode())
            #f.write(str(os.getpid()))

detection_progress=Process(target=detect_video_quality)
detection_progress.start()

result_progress=Process(target=read_progress_result)
result_progress.start()