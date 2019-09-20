#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 18:06
# @Author  : xingyue
# @File    : scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler


def schdeuler(log):
    scheduler = BackgroundScheduler()

    job_defaults = {
        'coalesce': False,
        'max_instances': 50,
        'misfire_grace_time':100,
    }
    scheduler.configure(job_defaults=job_defaults)
    scheduler._logger = log
    return  scheduler
