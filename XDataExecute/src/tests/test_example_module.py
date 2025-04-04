import unittest
import json
import os
from common.config import CreateConfigParent

# 创建一个示例配置类以便于测试
class ExampleConfig(metaclass=CreateConfigParent):
    data_container_name = 'example_container'

    def create(self, file_name):
        config = {
            'example_key': 'example_value'
        }
        with open(file_name, 'w+', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

class TestCreateConfigParent(unittest.TestCase):

    def setUp(self):
        """在每个测试用例之前运行，用于准备测试环境"""
        self.file_name = 'test_config.json'
        # 确保在每个测试前清理旧的配置文件
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def tearDown(self):
        """在每个测试用例之后运行，用于清理测试环境"""
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_example_config_creation(self):
        """测试 ExampleConfig 是否正确创建配置文件"""
        example_config = ExampleConfig()
        example_config.create(self.file_name)

        # 检查文件是否创建成功
        self.assertTrue(os.path.exists(self.file_name))

        # 读取文件内容并进行验证
        with open(self.file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(data['example_key'], 'example_value')

    def test_create_config_parent(self):
        """测试 CreateConfigParent 是否正确收集子类"""
        # 检查是否能获取到 'example_container'
        class_dict = CreateConfigParent.get_class_dic()
        self.assertIn('example_container', class_dict)
        self.assertIsInstance(class_dict['example_container'], ExampleConfig)

    def test_invalid_config_class(self):
        """测试未实现 required 方法的类"""
        with self.assertRaises(TypeError):
            class InvalidConfig(metaclass=CreateConfigParent):
                pass  # 没有实现 create 方法

if __name__ == '__main__':
    unittest.main()
