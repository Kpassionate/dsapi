#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created on: 2025/2/6 09:58   
Author:     guanyankai
"""
import multiprocessing

bind = "0.0.0.0:8888"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 300


"""
 gunicorn -c gunicorn.conf.py run:app
 
-c gunicorn.conf.py：使用 gunicorn.conf.py 文件中的配置。
run:app：加载 run.py 文件中的 app 实例。
"""