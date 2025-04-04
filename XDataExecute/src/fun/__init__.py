# 在 data_class_port.py 文件中
def get_convenient_class(cls, config_file):
    new_dict = {}
    for i in range(len(cls.convenient_class_list)):
        item = cls.convenient_class_list[i]
        if callable(item):  # 检查对象是否可调用
            new_dict[i] = item()  # 仅添加可调用对象的调用结果
        else:
            print(f"Warning: Item at index {i} is not callable.")
    return new_dict


# 在 __init__.py 文件中的 DataExecute 类的 __init__ 方法中
class DataExecute:
    def __init__(self, name: str, config_file=None):
        self.data_dic: dict = {'mysql': MysqlExecute(config_file),
                            'sqlite': SqlIteExecute(config_file),
                            'json': JsonExecute(config_file)}
        self.name = name
        # 更新 self.data_dic 时使用修改后的 get_convenient_class 方法
        self.data_dic.update(data_class_port.MyData.get_convenient_class(config_file))


# 其他部分代码保持不变
import os
import importlib.util
from abc import ABC, abstractmethod
from.data_class_port import *
from.sqlite_execute import *
from.mysql_execute import *
from.redis_execute import *
from.json_execute import *


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
folder_path = "./DataExecute"  # 假设 plug 文件夹与 main.py 在同一目录

# 导入 plug 文件夹中的所有类
import_classes_from_folder(folder_path)


class DataProt(ABC):
    data_vessel_select = MyData.get_class()
    dic = {'varchar (255)': "%s",
           'int': "%d"}

    def __init__(self, config_json_pth=None):
        if config_json_pth is None:
            config_json = GaiJson().gain('./data_config.json')
        else:
            config_json = GaiJson().gain(config_json_pth)
        self.config_json = config_json

    @abstractmethod
    def data_read_execute(self, form_name: str, screening_condition: str = None, field: str = None, data: dict = None):
        """
        :param form_name: 表单名称
        :param screening_condition: 筛选条件
        :param field: 字段
        :param data: 可选的额外数据
        :return:
        """
        pass

    @abstractmethod
    def data_deposit_execute(self, form_name: str, data: dict = None):
        """
        :param form_name: 表单名称
        :param data: 存入数据，字段名称为变量名
        :return:
        """
        pass


class MysqlExecute(DataProt):

    def data_read_execute(self, form_name: str, screening_condition: str = None, field: str = None, data: dict = None):
        condition = ''
        if screening_condition is not None:
            condition = f'WHERE {screening_condition}'
        if field:
            template = f'SELECT %s FROM {form_name} ' + condition
            return self.data_vessel_select['mysql'].execute(template % field)
        else:
            return self.data_vessel_select['mysql'].execute(f'SELECT * FROM {form_name} ' + condition)

    def data_deposit_execute(self, form_name: str, data: dict = None):
        # 建立字段映射字段
        field_dic = dict(zip([self.config_json.表单[i]['表单名称'] for i in self.config_json.表单],
                             [self.config_json.表单[j]['字段'][0] for j in self.config_json.表单]))
        exist_list = [i[0] for i in
                      self.data_vessel_select['mysql'].execute(f'SELECT {field_dic[form_name]} FROM {form_name}')]
        var = [j for j in self.config_json.表单 if self.config_json.表单[j]["表单名称"] == form_name][0]

        # 使用配置文件中的数据或提供的数据
        if data is None:
            data = {field: self.config_json.表单[var]["默认值"] for field in self.config_json.表单[var]["字段"]}

        if not data[self.config_json.表单[var]["字段"][0]] in exist_list:
            data_transmit = []  # 传递参数列表
            template_data1 = ''  # 表达式参数1
            template_data2 = ''  # 表达式参数
            template = f'insert into {form_name} (%s) values (%s)'  # 定义SQL表达式

            # 补全SQL表达式
            for j in tuple(self.config_json.表单[var]["字段"]):
                template_data1 += f'{j},'
            template_data1 = template_data1[:-1]
            for j in tuple("%s" if i == "int" else "%s" for i in tuple(self.config_json.表单[var]["类型"])):
                template_data2 += f'{j},'
            template_data2 = template_data2[:-1]

            for i in self.config_json.表单[var]["字段"]:  # 整理传递参数
                data_transmit.append(data[i])
            self.data_vessel_select['mysql'].execute(template % (template_data1, template_data2), *data_transmit)
        else:
            template = f'update {form_name} set %s where user = "{data[self.config_json.表单[var]["字段"][0]]}"'
            for i in list(data.keys())[1:]:
                if self.config_json.表单[var]["类型"][self.config_json.表单[var]['字段'].index(i)] == 'int':
                    self.data_vessel_select['mysql'].execute(template % f'{i} = {i}+%s', data[i])
                else:
                    self.data_vessel_select['mysql'].execute(template % f'{i}=%s', data[i])


class SqlIteExecute(DataProt):

    def data_read_execute(self, form_name: str, screening_condition: str = None, field: str = None, data: dict = None):
        condition = ''
        if screening_condition is not None:
            condition = f'WHERE {screening_condition}'
        if field:
            template = f'SELECT {"%s"} FROM {form_name} ' + condition
            return self.data_vessel_select['sqlite'].execute(template, field)
        else:
            return self.data_vessel_select['sqlite'].execute(f'SELECT * FROM {form_name} ' + condition)

    def data_deposit_execute(self, form_name: str, data: dict = None):
        # 建立字段映射字段
        field_dic = dict(zip([self.config_json.表单[i]['表单名称'] for i in self.config_json.表单],
                             [self.config_json.表单[j]['字段'][0] for j in self.config_json.表单]))
        exist_list = [i[0] for i in
                      self.data_vessel_select['sqlite'].execute(f'SELECT {field_dic[form_name]} FROM {form_name}')]
        var = [j for j in self.config_json.表单 if self.config_json.表单[j]["表单名称"] == form_name][0]

        # 使用配置文件中的数据或提供的数据
        if data is None:
            data = {field: self.config_json.表单[var]["默认值"] for field in self.config_json.表单[var]["字段"]}

        if not data[self.config_json.表单[var]["字段"][0]] in exist_list:
            data_transmit = []  # 传递参数列表
            template_data1 = ''  # 表达式参数1
            template_data2 = ''  # 表达式参数
            template = f'insert into {form_name} (%s) values (%s)'  # 定义SQL表达式

            # 补全SQL表达式
            for j in tuple(self.config_json.表单[var]["字段"]):
                template_data1 += f'{j},'
            template_data1 = template_data1[:-1]
            for j in tuple("%s" if i == "int" else "'%s'" for i in tuple(self.config_json.表单[var]["类型"])):
                template_data2 += f'{j},'
            template_data2 = template_data2[:-1]

            for i in self.config_json.表单[var]["字段"]:  # 整理传递参数
                data_transmit.append(data[i])
            self.data_vessel_select['sqlite'].execute(template % (template_data1, template_data2), *data_transmit)
        else:
            template = f'update {form_name} set %s where user = "{data[self.config_json.表单[var]["字段"][0]]}"'
            for i in list(data.keys())[1:]:
                if self.config_json.表单[var]["类型"][self.config_json.表单[var]['字段'].index(i)] == 'int':
                    self.data_vessel_select['sqlite'].execute(template % f'{i} = {i}+%s', data[i])
                else:
                    self.data_vessel_select['sqlite'].execute(template % f'{i}=%s', data[i])


class JsonExecute(DataProt):

    def data_read_execute(self, form_name: str, screening_condition: str = None, field: str = None, data: dict = None):
        json_data = self.data_vessel_select['json'].read()
        form_data = json_data.get(form_name, {})

        if screening_condition:
            key, value = screening_condition.split('==')
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            filtered_indices = [i for i, v in enumerate(form_data[key]) if v == value]
            return {k: form_data[k][filtered_indices] for k in form_data.keys()}

        if field:
            return {field: form_data[field]}

        return form_data

    def data_deposit_execute(self, form_name: str, data: dict = None):
        json_data = self.data_vessel_select['json'].read()
        if form_name not in json_data:
            json_data[form_name] = {}

        # 使用配置文件中的数据或提供的数据
        if data is None:
            var = [j for j in self.config_json.表单 if self.config_json.表单[j]["表单名称"] == form_name][0]
            data = {field: self.config_json.表单[var]["默认值"] for field in self.config_json.表单[var]["字段"]}

        for key in data.keys():
            if key not in json_data[form_name]:
                json_data[form_name][key] = []
            json_data[form_name][key].append(data[key])

        self.data_vessel_select['json'].write(json_data)


class DataExecute:
    def __init__(self, name: str, config_file=None):
        self.data_dic: dict = {'mysql': MysqlExecute(config_file),
                               'sqlite': SqlIteExecute(config_file),
                               'json': JsonExecute(config_file)}
        self.name = name
        # 更新 self.data_dic 时使用修改后的 get_convenient_class 方法
        self.data_dic.update(data_class_port.MyData.get_convenient_class(config_file))

    def data_read_execute(self, form_name: str, screening_condition: str = None, field: str = None):
        """

        :param form_name: 表单名称
        :param screening_condition: 限制表达式
        :param field: 字段
        :return:
        """
        # print(self.name)
        # print(screening_condition)
        return self.data_dic[self.name].data_read_execute(form_name, screening_condition, field)

    def data_deposit_execute(self, form_name: str, **data):
        """

        :param form_name: 表单名称
        :param data: 存入内容
        :return:
        """
        print(self.data_dic[self.name])
        self.data_dic[self.name].data_deposit_execute(form_name, data)