import yaml
import xlrd
from common import extractor,dir_base
import os


class ReadFile:
    config_dict = None

    @classmethod
    def get_config_dict(cls, config_path: str = 'config/config.yaml') -> dict:
        """读取配置文件，并且转换成字典
        :param config_path: 配置文件地址， 默认使用当前项目目录下的config/config.yaml
        return cls.config_dict
        """
        if cls.config_dict is None:
            # 指定编码格式解决，win下跑代码抛出错误
            with open(dir_base(config_path), 'r', encoding='utf-8') as file:
                cls.config_dict = yaml.load(file.read(), Loader=yaml.FullLoader)
        return cls.config_dict

    @classmethod
    def read_config(cls, expr: str = '.') -> dict:
        """默认读取config目录下的config.yaml配置文件，根据传递的expr jsonpath表达式可任意返回任何配置项
        :param expr: 提取表达式, 使用jsonpath语法,默认值提取整个读取的对象
        return 根据表达式返回的值
        """
        return extractor(cls.get_config_dict(), expr)

    @classmethod
    def read_testcase(cls):
        """
        读取excel格式的测试用例
        :return: data_list - pytest参数化可用的数据
        """
        data_list = []
        book = xlrd.open_workbook(dir_base(cls.read_config('$.file_path.test_case')))
        # 读取第一个sheet页
        table = book.sheet_by_index(0)
        for norw in range(1, table.nrows):
            # 每行第4列 是否运行
            if table.cell_value(norw, 5) != '否':  # 每行第4列等于否将不读取内容
                value = table.row_values(norw)
                value.pop(5)
                data_list.append(list(value))
        return data_list
