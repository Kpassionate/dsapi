#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created on: 2025/2/05 09:41   
Author:     guanyankai
"""
from pydantic import BaseModel, Field


class MyModel(BaseModel):
    model_name: str

    model_config = {
        'protected_namespaces': ()  # 禁用所有保护命名空间
    }


class BasePayload(MyModel):
    uid: str = Field(None, description="UID", example="456")
    conv_id: str = Field(None, description="会话ID", example="123")


class ConversationPayload(BasePayload):
    model_name: str = Field(None, description="模型名称", example="deepseek-r1:1.5b")
    input_text: str = Field(None, description="用户输入内容")


class PredictionPayload(ConversationPayload):
    sys_text: str = Field(None, description="系统预测内容")
