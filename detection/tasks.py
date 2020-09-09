from __future__ import absolute_import, unicode_literals
from celery import Celery
from ctypes import *
import time
from redis_queue import RedisQueue
from celery import shared_task
from multiprocessing import Pool, Process, Manager
import os
from detection.models import Video, Task, Error

vqd=cdll.LoadLibrary('/home/wells/VideoDetection/libvdq.so')
celery_app = Celery('a', broker='redis://localhost:6379/0')
task_queue = RedisQueue('tasks')
progress_list = RedisQueue('progressList')
result_list = RedisQueue('resultList')

@shared_task
def wrap_ctypes(video_id, file_path):
    file_path=file_path.encode()
    # print("使用celery")
    five = c_int * 16
    detection_item = five(0,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0)
    return vqd.Vqd(video_id, detection_item, file_path)

@shared_task
def test(n):
    print(n)

def detect_video_quality():
    #i=1
    while True:
        result = task_queue.get_nowait()
        if not result:
            continue
        result=result.decode().split("-")
        #print(result[1])
        new_video=Video(task=Task.objects.get(id=int(result[0])), video_name=result[1])
        new_video.save()
        wrap_ctypes.delay(new_video.id,result[1])
        #i=i+1

def read_progress_result():
    # f = open("data.txt",'a')
    while True:
        progress = progress_list.get_nowait()
        result=result_list.get_nowait()

        if progress:
            progress=progress.decode().split("-")
            progress_update=Video.objects.get(id=int(progress[0]))
            # print("id: %d"%int(progress[0]))
            print("progress: %f"%float(progress[1]))
            progress_update.detection_status=float(progress[1])
            progress_update.save()
            #print(os.getpid())
            #print("progress: "+progress.decode())
            #f.write(str(os.getpid()))
        if result:
            #print("result: "+result.decode())
            result=result.decode().split("-")
            error_num=(len(result)-3)/2
            i=2
            for m in range(int(error_num)):
                new_error=Error(video=Video.objects.get(id=int(result[0])), error_time=result[1], error_kind=result[i], error_info=result[i+1])
                new_error.save()
                i=i+2
            #print(os.getpid())
            
            #f.write(str(os.getpid()))

detection_progress=Process(target=detect_video_quality)
detection_progress.start()

result_progress=Process(target=read_progress_result)
result_progress.start()