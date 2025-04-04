# XDataExecute/fun/sqlite_execute

import sqlite3
from .data_class_port import MyData


class SqlIte(metaclass=MyData):
    data_name = 'sqlite'

    def __init__(self):
        self.database = None

    def execute(self, expression: str, *data):
        if self.database is None:
            self.database = f'./xbbot/data/{self.database}.db'
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute(expression, data)
        return_data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return return_data
