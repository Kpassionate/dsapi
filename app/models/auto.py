#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created on: 2025/2/05 19:14   
Author:     guanyankai
"""
from sqlalchemy import Column, Integer, String, TEXT
from sqlalchemy.ext.declarative import declarative_base

# 创建基本映射类
Base = declarative_base()


class CallRecord(Base):
    __tablename__ = "call_record"

    id = Column(Integer, primary_key=True)
    uid = Column(String(length=255), comment='用户UID')
    conv_id = Column(String(length=255), comment='会话ID')
    sys_text = Column(TEXT, comment='系统预测内容')
    input_text = Column(TEXT, comment='用户输入内容')
    assistant_content = Column(TEXT, comment='AI回复内容')
    # created_at = Column(String(length=255), comment='创建时间')

    # 定义表参数，包括指定使用的引擎
    __table_args__ = {'extend_existing': True, 'mysql_engine': 'InnoDB'}


