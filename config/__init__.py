# XDataExecute/config/__init__.py
from .creation_config import CreateConfigParent
from .create import *

def get_config_classes():
    rtn = {'mysql': MysqlConfig(),
            'sqlite': SqliteConfig(),
            'json': JsonConfig(),
            'redis': RedisConfig()}
    rtn.update(CreateConfigParent.get_class_dic())
    return rtn