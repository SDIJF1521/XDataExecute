# XDataExecute/config/creation_config.py

class CreateConfigParent(type):
    """
    自定义元类，确保子类实现特定的方法和属性。

    :param name: 子类的名称
    :param bases: 基类元组
    :param dic: 类的命名空间字典
    """

    data_name_list = []
    data_config_class = []

    def __new__(cls, name, bases, dic):
        if 'data_container_name' not in dic or not isinstance(dic['data_container_name'], str):
            raise TypeError('必须有data_container_name属性用于判断数据容器')

        if 'create' not in dic or not callable(dic['create']):
            raise TypeError('数据配置类类必须实现create方法用于生成配置文件')

        data_class = super().__new__(cls, name, bases, dic)
        cls.data_name_list.append(dic['data_container_name'])
        cls.data_config_class.append(data_class())
        return data_class

    @classmethod
    def get_class_dic(cls):
        """返回数据容器名称与配置类实例的字典"""
        return dict(zip(cls.data_name_list, cls.data_config_class))
