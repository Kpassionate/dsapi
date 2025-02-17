#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created on: 2025/2/11 09:24   
Author:     guanyankai
"""
import httpx
from httpx import HTTPStatusError, TimeoutException
from settings.log import error_logger
from utils.response_util import ErrorResponse


async def call_external_api(url, data):
    try:
        timeout = httpx.Timeout(120.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                url=url,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()  # 抛出HTTP错误
            response_data = response.json()
            return response_data
    except HTTPStatusError as e:
        error_logger.error(f"外部API调用失败, 状态码: {e.response.status_code}, 响应体: {e.response.text}")
        return ErrorResponse(code='500', message=f"外部API调用失败, 状态码: {e.response.status_code}")
    except TimeoutException:
        error_logger.error("外部API调用超时")
        return ErrorResponse(code='500', message="外部API调用超时")
    except Exception as e:
        error_logger.error(f"外部API调用失败: {str(e)}")
        return ErrorResponse(code='500', message=str(e))
