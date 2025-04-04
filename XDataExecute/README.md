# XDataExecute

## 项目介绍

  该项目旨在帮助开发者更轻松地进行数据操作目前提供了与 MySQL、Redis 和 SQLite 数据库json的简化交互接口，。库使用配置文件管理数据库连接信息，支持数据的读取和存储操作。

## 下载这个库

```shell
pip install XDataExecute
```

## 项目文件结构

```
your_project/
│
├── fun/
|   ├── __init__.py
│   ├── mysql_execute.py    # MySQL 数据库操作
│   ├── redis_execute.py     # Redis 数据库操作
│   └── sqlite_execute.py     # SQLite 数据库操作
│
├── config/
|   ├── __init__.py
│   ├── config_data.py       # 配置数据处理
│   └── ...                   # 其他配置处理库
│
├── CreateConfig.py
|
└── README.md                 # 本文档
```

## 库使用文档

### 配置

- 使用该库前我们需要进行一下简单的配置

  1. 在要主程序文件夹下我们要创建两个文件夹文件夹名称分别为 `DataExecute1` $数据容器拓展文件夹和$ `ConfigPlug`配置拓展文件夹
     2.在主程序文件夹下使用CreateConfig命令程序，CreateConfig命令程序语法如下：

  ```shell
  create-config <config_type> [--filename <file_name>]
  参数说明：
       1.config_type: 必填参数，表示你想要生成的配置文件类型。该值必须从配置类的可用类型中选择。
       2.--filename: 可选参数，指定生成的配置文件名。如果不提供该参数，则默认为 data_config.json。
  例：
       create-config mysql
  ```

  3. 配置文件书写
     - 对于生成的配置书写
       - 生成的mysql的配置文件内容如下：
         ```json
         {
           "数据库主机": "127.0.0.1",
           "数据库账号": "root",
           "数据库密码": "root",
           "数据库名称": "data_base_name",
           "表单": {
               "2表单": {
                   "表单名称": "1_table",
                   "字段": ["1_field", "2_field", "3_field", "4_field"],
                   "类型": ["varchar (255)", "int", "varchar (255)", "int"]
               },
               "1表单": {
                   "表单名称": "2_table",
                   "字段": ["1_field", "2_field", "3_field"],
                   "类型": ["varchar (255)", "int", "varchar (255)"]
               }
           }}
         ```
       - 这里我们需要提供数据库主机ip,数据库账号，密码，数据库名称以及数据库的表单及其字段，现在假设我们用一个如下表的数据库,其用户，密码为root，主机ip为127.0.0.1
         - <table>
               <tr>
                 <th>数据库名称</th>
                 <th>表单</th>
                 <th>字段</th>
                 <th>数据类型</th>
               </tr>
               <tr>
                 <td rowspan="10">XB</td>
                 <td rowspan="4">sign</td>
                 <td>user</td>
                 <td>varchar (255)</td>
               </tr>
               <tr>
                 <td>积分</td>
                 <td>int</td>
               </tr>
               <tr>
                 <td>日期</td>
                 <td>varchar (255)</td>
               </tr>
               <tr>
                 <td>天数</td>
                 <td>int</td>
               </tr>
               <tr>
                 <td rowspan="3">cq</td>
                 <td>user</td>
                 <td>varchar (255)</td>
               </tr>
               <tr>
                 <td>id</td>
                 <td>int</td>
               </tr>
               <tr>
                 <td>日期</td>
                 <td>varchar (255)</td>
               </tr>
               <tr>
                 <td rowspan="3">sgin</td>
                 <td>id</td>
                 <td>int</td>
               </tr>
               <tr>
                 <td>签诗</td>
                 <td>varchar (255)</td>
               </tr>
               <tr>
                 <td>签诗</td>
                 <td>varchar (255)</td>
               </tr>
         - 修改后的如下
           ```json
             {
               "数据库主机": "127.0.0.1",
               "数据库账号": "root",
               "数据库密码": "root",
               "数据库名称": "XB",
               "表单": {
                   "签到表单": {
                       "表单名称": "pd",
                       "字段": [
                           "user",
                           "积分",
                           "日期",
                           "天数"
                       ],
                       "类型": [
                           "varchar (255)",
                           "int",
                           "varchar (255)",
                           "int"
                       ]
                   },
                   "抽签表单": {
                       "表单名称": "cq",
                       "字段": [
                           "user",
                           "id",
                           "日期"
                       ],
                       "类型": [
                           "varchar (255)",
                           "int",
                           "varchar (255)"
                       ]
                   },
                   "存签表单": {
                       "表单名称": "sgin",
                       "字段": [
                           "id",
                           "签诗",
                           "意思"
                       ],
                       "类型": [
                           "int",
                           "varchar (255)",
                           "varchar (255)"
                       ]
                   }
               }}
           ```
         - 注意：$\color{red}{表单中的第一个字段为主键}$

### 便携查询

- 便携功能都依赖于配置文件，功能是通过配置文件来确定字段的正确，便捷方法都是使用DataExecute()类调用下面提供案例一及语法
  - 便携查询的的便捷函数是 `DataExecute()`$类的data_read_execute方法该方法的参数信息如下$
    ```python
    DataExecute(name, config_file).data_read_execute(form_name,creening_condition,field)
    '''
    name：容器名称，该参数为必填参数
    config_file：配置文件路径，该参数为必填参数该参数为可选参数不填时默认为None在不写时为路径为‘./dataconfig.json’
    form_name：表单名称,该参数为必填参数该参数为可选参数不填时默认为None在不写时为路径为全部表单
    creening_conditio：字段名，该参数为可选参数不填时默认为None在不写时为所有字段
    field：筛选条件，该参数为该参数为可选参数不填时默认为None
    '''
    ```

    - 现在假设配置文件如上我们要在mysql数据库内查找pd表内的所有数据我们可以这样来做
      ```python
      data = DataExecute('mysql').data_read_execute(form_name = 'pd')
      ```
    - 如果我们只要的是 `qd` $表单中的$ `user` $字段内容那么我们需要填写$ `creening_conditio` $参数$
      ```python
      data = DateExecute('mysql').data_read_execute(form_name = 'pd', creening_conditio=user)
      # 注意creening_conditio参数的内容要为字符串
      ```
    - 现在假设我们需要 `pd` $表单中的$`积分`$字段大于等于20的所有用户我们可以用如下代码$
      ```python
      data = DateExecute('mysql').data_read_execute(form_name = 'pd', creening_conditio=user, field = '积分 > 20')
      # 当我们在便捷查询方法中需要用到条件筛选查询时我们就要将field参数填写上，其内容为筛选的条件，数据类型要为字符串
      ```
    - 若我们的配置文件并不在当前文件夹下面或者配置文件的名称不为 `data_config.json` $那么我们需要将$ `config_file` $参数填写上用于定位配置文件的路径$
      ```python
      # 假设配置文件的在当前文件夹下且名称为sqilte.json
      data = DateExecute(name = 'mysql', config_file = './sqilte.json').data_read_execute(form_name = 'pd', creening_conditio=user,field = '积分 > 20')
      ```
- 提示：内置的其他数据容器的该方法使用一致

### 便携存储

- 便携查询的的便捷函数是 `DataExecute()`$类的$ `data_read_execute` $方法该方法的参数信息如下$
  ```python
  DataExecute(name, config_file).data_read_execute(form_name, data)
  '''
  name：容器名称，该参数为必填参数
  config_file：配置文件路径，该参数为必填参数该参数为可选参数不填时默认为None在不写时为路径为‘./dataconfig.json’
  form_name：表单名称,该参数为必填参数该参数为可选参数不填时默认为None在不写时为路径为全部表单
  data：必填参数,该参数是一个可变参数，其接受到的参数内容会转变为字典。参数名称为键.
  '''
  ```
- 现在以上述的mysql的配置为例，我们要在pd表中添加如下数据
  <table>
    <tr>
      <th>字段</th>
      <th>user</th>
      <th>积分</th>
      <th>日期</th>
      <th>天数</th>
    </tr>
    <tr>
      <td>数据</td>
      <td>12345678</td>
      <td>3</td>
      <td>2024-10-21</td>
      <td>1</td>
    </tr>
  </table>
- 那么我们可以使用如下的代码实现存储
  ```python
    DataExecute("mysql").data_read_execute(form_name = 'pd', user = "12345678", 积分 = 3, 日期 = "202-10-21", 天数 = 1)
  ```

  - 这里的参数如果属于可变参数的话要注意，参数的名称要为要存入的字段的名称
  - $如果我们要对某一个数据进行修改要看修改的是主键还是其他的内容，如果是主键那么我们需要使用高级存储来进行操作，如果是其他的内容那么\\写法如上，这里需要注意到是主键的参数和内容一定要写上，因为程序要基于主键的信息来判断进行修改还是创建操作$
  - 这里程序内置的容器用法一致

### 高阶使用方法

- 注意:高级查询的方法是使用元类的方法间接的调用容器类进行操作，我们不能直接使用容器类进行操作。并且在使用高阶方法是我们需要辨别要操作的是文件容器还是数据库，因为这两类的操作方法是不同的例如mysql的高阶操作借助 `execute`方法实现，而json的高阶操作借助 `read` 读取方法和 `deposit` 存入方法实现
- 调用容器类: 容器类的调用方法是使用 `MyData` $元类的$ `get_class` $方法$，容器操作类的具体调用方法如下
  ```python
  MyData.get_class(config_file)['name']
  '''
  config_file: 配置文件路径
  name: 容器名称
  '''
  ```

  - 该方法会返回一个实例化字典，具体要使用那个容器类就通过字典的key进行获取就可以

#### 读取

- 读取数据是指从数据库或数据容器中获取信息。使用 MyData 元类的方法，可以轻松获取容器类的实例，并进行数据的读取操作。以下是一个示例代码，展示如何读取指定容器的数据：

```python
# 假设我们已经在配置文件中定义了数据库容器
container = MyData.get_class(config_file)['mysql']  # 获取MySQL容器类实例
data = container.execute("SELECT * FROM pd")  # 执行SQL查询，读取所有数据
print(data)  # 输出查询结果
```

- 读取JSON数据可以通过以下方式实现：

```python
# 获取JSON容器类实例
json_container = MyData.get_class(config_file)['json']
data = json_container.read()  # 从指定JSON文件中读取数据
print(data)  # 输出读取的JSON数据
```

- 只要redis数据库的高阶操作用法和redis库一样，execute方法后面要更上redis库的具体操作函数如set

```python
Redis = MyData.get_class(config_file)['redis']
Redis.execute().set(key, value)
'''
key: 键
value：值
'''
```

#### 存储

- SQL数据库存入示例

```python
# 假设我们已经在配置文件中定义了MySQL容器
mysql_container = MyData.get_class(config_file)['mysql']  # 获取MySQL容器类实例
mysql_container.execute("INSERT INTO pd (user, 积分, 日期, 天数) VALUES (%s, %s, %s, %s)", 
                        ('12345678', 3, '2024-10-21', 1))  # 向pd表中插入数据

```

- json文件容器的存储要借助 `deposit` 存入方法下面提供示例

```python
 #假设我们已经在配置文件中定义了json容器
 json =  MyData.get_class(config_file)['json']  # 获取json容器类实例
 dic = json.read()
 dic.update({1:2})
 json.deposit(dic)
```

- redis请参考redis库

#### 编码补全提示

- 我们在编写代码时如果需要编码补全请在获取容器时将调用的容器名称设置为变量例如

```python
mysql = MyData.get_class(config_file)['mysql']
sqlite = MyData.get_class(config_file)['msqlite']
```

### 拓展库

#### 拓展容器类

#### 拓展操作类
