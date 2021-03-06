import redis

class RedisQueue(object):
    def __init__(self, name, **redis_kwargs):
       # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
       self.__db= redis.Redis(host='localhost' ,port=6379 ,password='')
       self.key = name

    def qsize(self):
        return self.__db.llen(self.key)  # 返回队列里面list内元素的数量

    def put(self, item):
        self.__db.rpush(self.key, item)  # 添加新元素到队列最右方

    def get_wait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.__db.blpop(self.key, timeout=timeout)
        # if item:
        #     item = item[1]  # 返回值为一个tuple
        return item

    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__db.lpop(self.key)  
        return item
    
    def get_all_keys(self):
        return self.__db.keys()

    def remove_all(self):
        keys=self.__db.keys()
        if len(keys)==0:
            return
        self.__db.delete(*keys)