#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from fastapi.responses import JSONResponse
from starlette import status


def CreateSuccess():
    data = {
        'code': '200',
        'message': 'Create Success'
    }
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=data)


def CreateFail():
    data = {
        'code': '500',
        'message': 'Create Fail'
    }
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=data)


def UpdateSuccess():
    data = {
        'code': '200',
        'message': 'Update Success'
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


def UpdateFail():
    data = {
        'code': '500',
        'message': 'Update Fail'
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


def SuccessResponse(result: dict):
    data = {
        'code': '200',
        **result,
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


def ErrorResponse(code, message):
    data = {
        'code': code,
        'message': message
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)

