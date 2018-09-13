#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/7 11:21
# @Author  : xingyue
# @File    : userfile.py
import os


def userList():
    files = []
    project_dir = os.path.dirname(os.path.abspath(__file__))
    userdir = os.path.join(os.path.dirname(project_dir),'users')
    filecount = os.listdir(userdir)
    for file in filecount:
        filepath = os.path.join(userdir,file)
        count = len(open(filepath, 'rU').readlines())
        a= [file,count]
        files.append(a)
    return files