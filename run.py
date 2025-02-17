#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created on: 2025/2/05 18:38   
Author:     guanyankai
"""

import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.view import application
from settings.db_config import engines
from settings.middleware import LoggingMiddleware

app = FastAPI(
    title='DeepSeek API Docs',
    description='Ollama DeepSeek',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redocs',
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 挂载模板目录
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):  # call_next将接收request请求做为参数
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)  # 添加自定义的以“X-”开头的请求头
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.include_router(application, prefix='/api', tags=['DS API'])


@app.on_event("shutdown")
async def shutdown_event():
    # 关闭所有数据库引擎
    for engine in engines.values():
        try:
            await engine.dispose()
        except Exception as e:
            # print(f"Error while disposing engine: {e}")
            ...


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("run:app", host='0.0.0.0', port=8088, reload=True, workers=1)
