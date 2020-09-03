from multiprocessing import Pool, Process, Value,Lock
from multiprocessing.managers import BaseManager
import time
import os

class Node:
    def __init__(self, item):
        self.item=item
        self.next=None

class TaskList:
    def __init__(self):
        self.head=None
        self.tail=self.head
    def empty(self):
        if (self.head is None) & (self.tail is None):
            return True
        else:
            return False
    def append(self, item):
        if self.empty():
            self.head=Node(item)
            self.tail=self.head
        else:
            self.tail.next=Node(item)
            self.tail=self.tail.next
    def pop(self):
        if self.empty():
            return

        tmp_item=self.head.item
        tmp_node=self.head.next
        if self.head is self.tail:
            self.tail=None
        self.head=None
        self.head=tmp_node
        return tmp_item

class VideoQualityDeteciton:
    def __init__(self, process_num):
        BaseManager.register('TaskList', TaskList)
        manager = BaseManager()
        manager.start()

        self.task_list=manager.TaskList()
        self.process_num=process_num
        pool_process=Process(target=self.make_process_pool, args=[self.task_list])
        pool_process.start()

    def make_process_pool(self, task_list):
        process_pool=Pool(processes=self.process_num)
        while True:
            if task_list.empty():
                continue
            else:
                process_pool.apply_async(self.test ,(self.task_list.pop(),))
    def test(i):
        print(i)
        time.sleep(5)

vqd=VideoQualityDeteciton(2)

vqd.task_list.append(1)
vqd.task_list.append(2)
vqd.task_list.append(5)
vqd.task_list.append("wells")

time.sleep(20)
vqd.task_list.append(1)
vqd.task_list.append(2)
vqd.task_list.append(5)
vqd.task_list.append("wells")
# task_list=TaskList()
# task_list.append(1)
# task_list.append(2)
# task_list.append(5)
# task_list.append("wells")

# t=task_list.pop()
# t=task_list.pop()
# t=task_list.pop()
# t=task_list.pop()
# t=task_list.pop()
# task_list.append(2)
# task_list.append(0)