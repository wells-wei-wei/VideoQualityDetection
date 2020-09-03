from celery import Celery
from ctypes import *
import time
from redis_queue import RedisQueue
from celery import shared_task

vqd=cdll.LoadLibrary('/home/wells/VideoDetection/libvdq.so')
celery_app = Celery('a', broker='redis://localhost:6379/0')
task_queue = RedisQueue('tasks')

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