#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created on: 2025/2/05 11:27
Author:     guanyankai
"""
import json
import time
import traceback
from fastapi import Request
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from .log import app_logger, error_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_time = datetime.now()
        st = time.time()
        req_json = ""
        if request.method == "POST":
            req_json = await request.json()
        # 响应异常处理
        try:
            response = await call_next(request)
        except Exception:
            traceback_info = traceback.format_exc()
            error_response = {
                "code": "500",
                "msg": "服务器异常",
                "detail": traceback_info
            }
            error_logger.error(traceback_info)
            response = JSONResponse(status_code=500, content=error_response)
        latency = f"{round((st - time.time()), 3)} s"
        # 记录请求信息
        log_data = {
            "clientIp": request.client.host,  # 客户端IP
            "apiPath": str(request.url),  # 请求PATH
            "requestMethod": request.method,  # 请求方法
            "requestTime": str(request_time),  # 请求时间
            "totalLatency": latency,  # 请求延迟
            "request": req_json,  # 请求内容
            "response": '{}',  # content 返回数据
            "statusCode": str(response.status_code),  # 返回状态码
        }
        app_logger.info(json.dumps(log_data))
        return response
