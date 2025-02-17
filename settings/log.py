#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created on: 2025/2/05 11:27
Author:     guanyankai
"""
import os
import logging
from logging.handlers import RotatingFileHandler

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 配置 error 日志
error_logger = logging.getLogger("error_log")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(os.path.join(log_dir, "error.log"))
error_format = logging.Formatter('%(levelname)s %(asctime)s [%(module)s:%(funcName)s] %(message)s')
error_handler.setFormatter(error_format)
error_logger.addHandler(error_handler)

# 配置应用程序日志
app_logger = logging.getLogger("my_app")
app_logger.setLevel(logging.INFO)
log_handler = RotatingFileHandler(os.path.join(log_dir, "app.log"), maxBytes=1024 * 1024 * 10, backupCount=10)
log_formatter = logging.Formatter('%(levelname)s %(asctime)s [%(module)s:%(funcName)s] %(message)s')
log_handler.setFormatter(log_formatter)
app_logger.addHandler(log_handler)
