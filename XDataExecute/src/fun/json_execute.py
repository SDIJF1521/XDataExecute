# XDataExecute/fun/json_execute.py

import json
from .data_class_port import MyData


class Json(metaclass=MyData):
    data_name = 'json'

    def __init__(self):
        self.file = None

    def read(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            print('yes')
            json_data = json.load(f)
            print(dict(json_data))
            return dict(json_data)

    def deposit(self, data: dict):
        with open(self.file, 'w+', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
