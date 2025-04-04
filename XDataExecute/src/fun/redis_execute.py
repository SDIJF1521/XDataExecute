import redis
import logging
from common.config.config_data import GaiJson
from .data_class_port import MyData

# 配置日志记录
logging.basicConfig(level=logging.INFO)


class Redis(metaclass=MyData):
    data_name = 'redis'

    def __init__(self):
        self.host = None
        self.port = None

    def execute(self):
        if self.host is None:
            self.host = GaiJson().gain().redis设置['redis-host']
        if self.port is None:
            self.port = GaiJson().gain().redis设置['redis-port']
        password = GaiJson().gain().redis设置.get('redis-password', None)
        db = GaiJson().gain().redis设置.get('redis-db', 0)

        pool = redis.ConnectionPool(
            host=self.host,
            port=self.port,
            password=password,
            db=db,
            decode_responses=True
        )

        return redis.Redis(connection_pool=pool)

    def data_read_execute(self, form_name: str, screening_condition: str = None, field: str = None):
        try:
            r = self.execute()
            keys = r.keys(f"{form_name}:*")
            results = []

            for key in keys:
                value = r.hgetall(key)
                if screening_condition:
                    if self.check_condition(value, screening_condition):
                        results.append(value)
                else:
                    results.append(value)

            if field:
                return [{field: result.get(field)} for result in results]

            return results if results else None  # 返回空列表或 None

        except Exception as e:
            logging.error(f"读取数据时出错: {e}")
            return None

    def data_deposit_execute(self, form_name: str, data: dict = None):
        if data is None or 'id' not in data:
            logging.error("存储数据失败: 提供的数据为空或缺少 'id' 字段")
            return

        try:
            r = self.execute()
            key = f"{form_name}:{data['id']}"

            if r.exists(key):
                logging.warning(f"数据已经存在, 更新数据: {data} 到 {key}")
            else:
                logging.info(f"存储数据: {data} 到 {key}")

            var = self.get_form_index(form_name)

            if var is None:
                logging.error(f"找不到表单名称: {form_name}")
                return

            field_dic = self.get_field_mapping(form_name)

            mapped_data = {field_dic[form_name]: data['id']}
            for field in self.config_json.表单[var]["字段"]:
                mapped_data[field] = data.get(field, self.config_json.表单[var]["默认值"])

            r.hset(key, mapping=mapped_data)
            logging.info(f"成功存储数据: {mapped_data} 到 {key}")

        except Exception as e:
            logging.error(f"存储数据时出错: {e}")

    def get_form_index(self, form_name: str):
        """ 获取表单的索引，如果表单不存在返回 None """
        try:
            return self.config_json.表单.index(form_name)
        except ValueError:
            return None

    def get_field_mapping(self, form_name: str):
        """ 获取字段映射字典 """
        return dict(zip(
            [self.config_json.表单[i]['表单名称'] for i in range(len(self.config_json.表单))],
            [self.config_json.表单[j]['字段'][0] for j in range(len(self.config_json.表单))]
        ))

    def check_condition(self, value: dict, condition: str) -> bool:
        # 实现条件的解析和检查逻辑
        # 示例：将条件转为一个可执行的函数
        return True  # 这里返回 True 表示条件匹配，实际实现需替换
