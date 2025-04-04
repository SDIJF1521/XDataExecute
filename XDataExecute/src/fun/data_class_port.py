# XDataExecute/fun/data_class_port.py
import inspect


# 定义数据容器控制类创建元类
class MyData(type):
    data_name_list = []
    data_class_list = []
    convenient_name_list = []
    convenient_class_list = []

    def __new__(cls, name, bases, dic):
        # 类名规范命名禁止蛇形命名
        if '_' in name:
            raise TypeError("数据类的名称不能有‘_’")
        if not callable(dic.get('data_name')) and ('data_name' not in dic or not isinstance(dic['data_name'], str)):
            raise ValueError("‘data_name’属性必须存在并且数据类型要为str，用于判断当前类的数据管理容器")
        # 禁止帕斯卡命名法
        if any(char.isupper() for char in dic):
            raise TypeError('属性和方法的命名不能有大写')
        if dic['data_name'] in cls.data_name_list and not callable(dic.get('data_name')):
            raise ValueError('‘data_name’属性的值在data_name_list列表中已存在')
        data_class = super().__new__(cls, name, bases, dic)
        cls.data_class_list.append(data_class())
        cls.data_name_list.append(dic['data_name'])
        if not callable(dic.get('execute')) and (not callable(dic.get('read')) and not callable(dic.get('deposit'))):
            raise TypeError('必须有execute操作方法或deposit存入方法和read读取方法')
        if callable(dic.get('data_read_execute')) and callable(dic.get('data_deposit_execute')):
            cls.convenient_name_list.append(dic['data_name'])
            cls.convenient_class_list.append(data_class)
        return data_class

    @classmethod
    # 调用字典
    def get_class(cls):
        return dict(zip(cls.data_name_list, cls.data_class_list))

    @classmethod
    def get_convenient_class(cls, config_file=None):
        for i in range(len(cls.convenient_class_list)):
            print(cls.convenient_class_list[i]())
            signature = inspect.signature(cls.convenient_class_list[i].__init__)
            if 'config_file' in signature.parameters:
                if not config_file is None:
                    cls.convenient_class_list[i] = cls.data_class_list[i](config_file)
                else:
                    cls.convenient_class_list[i] = cls.convenient_class_list[i]()
            else:
                cls.convenient_class_list[i] = cls.convenient_class_list[i]()
        return dict(zip(cls.convenient_name_list, cls.convenient_class_list))