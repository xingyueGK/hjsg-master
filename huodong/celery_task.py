# -*- coding:utf-8 -*-

from celery import  Celery

broker = 'redis://127.0.0.1:6379/7'
backend = 'redis://127.0.0.1:6379/8'

app = Celery('test',broker=broker,backend=backend)

@app.task
def a():
    print 'aaaaaaaaaaaaaaaaaaa'

