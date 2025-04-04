# XDataExecute/config/create.py

import os
import json
import importlib.util
from common.config.creation_config import CreateConfigParent
from abc import ABC, abstractmethod


def import_classes_from_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                file_path = os.path.join(root, file)
                import_classes_from_file(file_path)


def import_classes_from_file(file_path):
    # 提取模块名称
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    # 动态加载模块
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 将模块中的所有类导入到当前全局命名空间中
    for name, cls in module.__dict__.items():
        if isinstance(cls, type):
            globals()[name] = cls


# 指定 plug 文件夹路径
folder_path = "./ConfigPlug"  # 假设 plug 文件夹与 CreateConfig.py 在同一目录

# 导入 plug 文件夹中的所有类
import_classes_from_folder(folder_path)


# 定义策略接口
class DataConfig(ABC):
    @abstractmethod
    def create(self, file_name):
        confing = {}


# sqlite存储配置

class SqliteConfig(DataConfig):
    def create(self, file_name):
        config = {'数据库名称': 'XB',
                  '表单': {
                      '1表单': {
                          '表单名称': '1_table',
                          '字段': ['1_field', '2_field', '3_field', '4_field'],
                          '类型': ['varchar (255)', 'int', 'varchar (255)', 'int']
                      },
                      '2表单': {
                          '表单名称': '2_table',
                          '字段': ['1_field', '2_field', '3_field'],
                          '类型': ['varchar (255)', 'int', 'varchar (255)']
                      }
                  }}
        with open('data_config.json', 'w+', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)


# mysql存储配置

class MysqlConfig(DataConfig):
    def create(self, file_name):
        config = {
            '数据库主机': '127.0.0.1',
            '数据库账号': 'root',
            '数据库密码': 'root',
            '数据库名称': 'data_base_name',
            '表单': {
                '2表单': {
                    '表单名称': '1_table',
                    '字段': ['1_field', '2_field', '3_field', '4_field'],
                    '类型': ['varchar (255)', 'int', 'varchar (255)', 'int']
                },
                '1表单': {
                    '表单名称': '2_table',
                    '字段': ['1_field', '2_field', '3_field'],
                    '类型': ['varchar (255)', 'int', 'varchar (255)']
                }
            }}
        with open(file_name, 'w+', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)


# json存储配置

class JsonConfig(DataConfig):
    def create(self, file_name):
        config = {
            '文件名称': 'name',
            '表单': {
                '1表单': {
                    '表单名称': '1_table',
                    '字段': ['1_field', '2_field', '3_field', '4_field']
                },
                '2表单': {
                    '表单名称': '2_table',
                    '字段': ['1_field', '2_field', '2_field']
                }
            }}
        with open(file_name, 'w+', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)


# redis
class RedisConfig(DataConfig):
    def create(self, file_name):
        config = {"redis设置": {
                                "redis-host": "127.0.0.1",
                                "redis-port": 6379,
                                "redis-password": None,
                                "redis-db": 0
                                },
                    '表单': {
                            '1表单': {
                                '表单名称': '1_table',
                                '字段': ['1_field', '2_field', '3_field', '4_field']
                            },
                            '2表单': {
                                '表单名称': '2_table',
                                '字段': ['1_field', '2_field', '2_field']
                            }
                    }}
        with open(file_name, 'w+', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)


# 数据存储配置上下文类

class DataConfigFile:
    def __init__(self, kind: DataConfig | CreateConfigParent, file_name):
        self.kind = kind
        self.file_name = file_name

    def execute(self):
        self.kind.create(self.file_name)
