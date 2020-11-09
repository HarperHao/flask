"""
Author   : HarperHao
TIME    ： 2020/11/8
FUNCTION:  Local对象的学习
"""
from threading import Thread
from werkzeug.local import Local

local = Local()
local.request = '123'


class MyThread(Thread):
    def run(self):
        local.request = 'abc'
        print("子线程:", local.request)


mythread = MyThread()
mythread.start()
mythread.join()

print('主线程：', local.request)
