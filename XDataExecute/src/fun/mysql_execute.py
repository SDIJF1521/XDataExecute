# XDataExecute/fun/mysql_execute.py

import pymysql
from common.config.config_data import GaiJson
from .data_class_port import MyData


class Mysql(metaclass=MyData):
    data_name = 'mysql'

    def __init__(self,config_json=None):
        self.json = GaiJson().gain(config_json)
        self.host = None
        self.user = None
        self.password = None
        self.database = None
    def execute(self, expression: str, *data):
        if self.host is None:
            self.host = self.json.数据库主机
        if self.user is None:
            self.user = self.json.数据库账号
        if self.password is None:
            self.password = self.json.数据库密码
        if self.database is None:
            self.database = self.json.数据库名称
        print(self.host,self.user,self.password,self.database)
        conn = pymysql.connect(host=self.host,
                               user=self.user,
                               password=self.password,
                               database=self.database
                               )
        cursor = conn.cursor()
        # print(expression%data)
        if data:
            cursor.execute(expression, data)
        else:
            cursor.execute(expression)
        return_data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return return_data
