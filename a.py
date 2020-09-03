from celery import Celery
from ctypes import *
import time
from redis_queue import RedisQueue

vqd=cdll.LoadLibrary('/home/wells/VideoDetection/libvdq.so')
celery_app = Celery('a', broker='redis://localhost:6379/0')
task_queue = RedisQueue('tasks')

@celery_app.task
def wrap_ctypes(video_id, file_path):
    file_path=file_path.encode()
    print("使用celery")
    five = c_int * 16
    detection_item = five(0,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0)
    return vqd.Vqd(video_id, detection_item, file_path)

@celery_app.task
def test(n):
    print(n)

if __name__ == '__main__':
    i=1
    while True:
        result = task_queue.get_nowait()
        if not result:
            continue
        wrap_ctypes.delay(i,result.decode())
        i=i+1