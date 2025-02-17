#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created on: 2025/2/05 11:27
Author:     guanyankai
"""

import warnings
import pandas as pd
import pymysql

warnings.filterwarnings('ignore')


class DATABASES(object):
    def __init__(self, mysql_database, is_online):
        self.base = mysql_database['default']
        self.IS_ONLINE = is_online
        self.db_params = {
            'host': self.base['HOST'],
            'port': self.base['PORT'],
            'user': self.base['USER'],
            'password': self.base['PASSWORD'],
            'db': self.base['NAME']
        }

    @staticmethod
    def get_db_option(country):
        options = "set time_zone='{time_zone}', group_concat_max_len=4294967295;"
        if country == 'In':
            options = options.format(time_zone='+5:30')
        elif country == 'CH':
            options = options.format(time_zone='America/Santiago')
        else:
            options = options.format(time_zone='+8:00')
        return options

    def init(self):
        # 此处可修改为读取MYSQL获取N个数据库连接信息
        databases_conn = {'auto': 'mysql+pymysql://root:g1234567@127.0.0.1/auto'}
        return databases_conn

