from __future__ import absolute_import, unicode_literals
from celery import Celery
from ctypes import *
import time
from redis_queue import RedisQueue
from celery import shared_task
from celery.result import AsyncResult
from multiprocessing import Pool, Process, Manager
import os
from detection.models import Video, Task, Error
from django.utils import timezone


vqd=cdll.LoadLibrary('/home/wells/VideoDetection/libvdq.so')
celery_app = Celery('a', backend="amqp", broker='redis://localhost:6379/0')
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

class Task_Manager():
    def __init__(self):
        self.task_video={}
        self.video_task={}
        self.video_worker={}
    def get_worker_num(self):
        return len(self.video_worker)

    def add_new_video(self, task_id, video_id, video_num):
        if self.task_video.__contains__(task_id) is False:
            self.task_video.setdefault(task_id,video_num)
        self.video_task.setdefault(video_id, task_id)
        # self.task_video[task_id]=self.task_video[task_id]-1
    def add_video_worker(self, video_id, worker_id):
        self.video_worker.setdefault(video_id, worker_id)
    def check_task(self):
        for key in list(self.video_worker.keys()):
            #print(self.video_worker[key])
            res = AsyncResult(self.video_worker[key])
            if res.ready():
                self.video_worker.pop(key)
                current_task_id=self.video_task[key]
                self.video_task.pop(key)
                self.task_video[current_task_id]=self.task_video[current_task_id]-1
                if self.task_video[current_task_id] is 0:
                    task_finish_update=Task.objects.get(id=current_task_id)
                    task_finish_update.finish_time=timezone.now()
                    task_finish_update.save()
                    self.task_video.pop(current_task_id)
                    print("任务 "+str(current_task_id)+" 完成")




def detect_video_quality():
    #i=1
    task_manager=Task_Manager()
    while True:
        task_manager.check_task()
        if len(task_queue.get_all_keys())!=0 and task_queue.qsize()==0 and progress_list.qsize()==0 and result_list.qsize()==0 and task_manager.get_worker_num()==0:
            print(len(task_queue.get_all_keys()))
            task_queue.remove_all()
        result = task_queue.get_nowait()
        if not result:
            continue
        result=result.decode().split("-")
        #print(result[1])
        new_video=Video(task=Task.objects.get(id=int(result[0])), video_name=result[1])
        new_video.save()

        task_manager.add_new_video(int(result[0]),new_video.id, Task.objects.get(id=int(result[0])).video_num)
        
        worker=wrap_ctypes.delay(new_video.id,result[1])

        task_manager.add_video_worker(new_video.id,worker.task_id)
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