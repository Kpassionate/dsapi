#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created on: 2025/2/05 13:36
Author:     guanyankai
"""
import pymysql
from .dev import MYSQL_DATABASES, IS_ONLINE
from .db import DATABASES
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

pymysql.install_as_MySQLdb()

db_connect_dict = DATABASES(mysql_database=MYSQL_DATABASES, is_online=IS_ONLINE).init()
engines = {}
db_session = {}
for db_connect in db_connect_dict:
    # echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
    engine = create_engine(db_connect_dict[db_connect], echo=False, pool_size=3)
    engines[db_connect] = engine
    Session = sessionmaker(bind=engine)
    db_session[db_connect] = Session()

print(f"数据库链接数：{db_session.__len__()}")
