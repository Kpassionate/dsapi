#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created on: 2025/2/05 18:06   
Author:     guanyankai
"""
from fastapi import APIRouter
from app.models.auto import CallRecord
from settings.db_config import db_session
from app.payload import ConversationPayload, PredictionPayload
from utils.external_api import call_external_api
from utils.response_util import SuccessResponse, ErrorResponse

application = APIRouter(prefix='/ds')
OLLAMA_URL = "http://localhost:11434/api/chat"


@application.get("/get_record/{conv_id}", summary="获取会话记录")
async def get_record(conv_id: str):
    records = db_session['auto'].query(CallRecord).filter(
        CallRecord.conv_id == conv_id).order_by(CallRecord.id.desc()).limit(10)
    data = [
        {
            'conv_id': record.conv_id,
            'input_text': record.input_text,
            'assistant_content': record.assistant_content
        } for record in records
    ]
    return SuccessResponse({'data': data})


@application.post("/create_conversation/", summary="创建会话")
async def create_conversation(payload: ConversationPayload):
    payload = dict(payload)
    uid = payload.get('uid')
    conv_id = payload.get('conv_id')
    model_name = payload.get('model_name', '').strip()
    input_text = payload.get('input_text', '').strip()
    if not all([uid, conv_id, model_name, input_text]):
        return ErrorResponse(code='400', message="输入不能为空")
    # 构造请求参数
    data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": input_text}
        ],
        "stream": False
    }
    # 调用外部API
    response_data = await call_external_api(OLLAMA_URL, data)
    if hasattr(response_data, 'code'):
        return response_data
    assistant_content = response_data.get('message', {}).get('content', '响应内容为空')
    # 保存到数据库
    record = CallRecord(
        uid=uid, conv_id=conv_id, input_text=input_text, sys_text='', assistant_content=assistant_content)
    with db_session['auto'] as session:
        session.add(record)
        session.commit()
    return SuccessResponse(response_data)


@application.post("/continue_conversation/", summary="连续对话")
async def continue_conversation(payload: ConversationPayload):
    payload = dict(payload)
    uid = payload.get('uid')
    conv_id = payload.get('conv_id')
    model_name = payload.get('model_name', '').strip()
    input_text = payload.get('input_text', '').strip()
    if not all([uid, conv_id, model_name, input_text]):
        return ErrorResponse(code='400', message="输入不能为空")
    # 获取近三次请求对话
    records = db_session['auto'].query(CallRecord).filter(
        CallRecord.conv_id == conv_id).order_by(CallRecord.id.desc()).limit(3)
    # 构造连续对话message
    messages = []
    for record in records[::-1]:
        messages.append({'role': 'user', 'content': record.input_text})
        messages.append({'role': 'assistant', 'content': record.assistant_content})
    messages.append({'role': 'user', 'content': input_text})
    print(messages)
    # 构造请求参数
    data = {
        "model": model_name,
        "messages": messages,
        "stream": False
    }
    response_data = await call_external_api(OLLAMA_URL, data)
    if hasattr(response_data, 'code'):
        return response_data
    assistant_content = response_data.get('message', {}).get('content', '响应内容为空')
    record = CallRecord(
        uid=uid, conv_id=conv_id, input_text=input_text, sys_text='', assistant_content=assistant_content)
    with db_session['auto'] as session:
        session.add(record)
        session.commit()
    return SuccessResponse(response_data)


@application.post("/create_prediction/", summary="预测会话")
async def create_prediction(payload: PredictionPayload):
    payload = dict(payload)
    uid = payload.get('uid')
    conv_id = payload.get('conv_id')
    input_text = payload.get('input_text', '').strip()
    model_name = payload.get('model_name', '').strip()
    sys_text = payload.get('sys_text', '').strip()
    if not all([uid, conv_id, model_name, input_text]):
        return ErrorResponse(code='400', message="输入不能为空")
    # 构造请求参数
    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": sys_text},
            {"role": "user", "content": input_text}
        ],
        "stream": False
    }
    response_data = await call_external_api(OLLAMA_URL, data)
    if hasattr(response_data, 'code'):
        return response_data
    assistant_content = response_data.get('message', {}).get('content', '响应内容为空')
    record = CallRecord(
        uid=uid, conv_id=conv_id, input_text=input_text, sys_text=sys_text, assistant_content=assistant_content)
    with db_session['auto'] as session:
        session.add(record)
        session.commit()
    return SuccessResponse(response_data)
