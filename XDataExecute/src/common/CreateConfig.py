# XDataExecute/CreateConfig.py

import argparse
from .config import get_config_classes
from .config.create import DataConfigFile


def main():
    config_classes = get_config_classes()
    config_names = config_classes.keys()

    parser = argparse.ArgumentParser(description="生成配置文件的命令行工具")
    parser.add_argument(
        "config_type",
        choices=config_names,
        help="要生成的配置文件类型"
    )

    # 添加一个可选参数，接受文件名，默认值为 data_config.json
    parser.add_argument(
        "--filename",
        default="data_config.json",
        help="生成的配置文件名称（默认为 data_config.json）"
    )

    args = parser.parse_args()

    # 获取选定的配置类
    config_class = config_classes.get(args.config_type)

    if config_class is None:
        print(f"错误: 找不到配置类型 {args.config_type}")
        return

    # 创建配置文件
    DataConfigFile(config_class, args.filename).execute()  # 传递文件名
    print(f"配置文件已生成: {args.filename}")


if __name__ == "__main__":
    main()
