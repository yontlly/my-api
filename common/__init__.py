import json
import re

import allure
import uuid
import time
from jsonpath import jsonpath
from loguru import logger
import os
import base64


'''
调用数据池数据
'''
def extractor(obj: dict, expr: str = '.') -> object:
    """
    根据表达式提取字典中的value，表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
    :param obj :json/dict类型数据
    :param expr: 表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
    $.0.1 提取字典中的第一个列表中的第二个的值
    """
    try:
        result = jsonpath(obj, expr)[0]
    except Exception as e:
        logger.error(f'提取不到内容，丢给你一个错误！{e}')
        result = None
    return result


def dir_base(*fileName):
    '''
    :param fileName:path of file,name of file
    :return: 绝对路径
    '''
    return os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), *fileName)



# def rep_expr(content: str, data: dict, expr: str = '&(.*?)&') -> str:
#     """从请求参数的字符串中，使用正则的方法找出合适的字符串内容并进行替换
#     :param content: 原始的字符串内容
#     :param data: 在该项目中一般为响应字典，从字典取值出来
#     :param expr: 查找用的正则表达式
#     return content： 替换表达式后的字符串
#     """
#     for ctt in re.findall(expr, content):
#         content = content.replace(f'&{ctt}&', str(extractor(data, ctt)))
#
#     return content
def rep_expr(content: str, data: dict, expr: str = '&(.*?)&') -> str:
    """从请求参数的字符串中，使用正则的方法找出合适的字符串内容并进行替换
    :param content: 原始的字符串内容
    :param data: 在该项目中一般为响应字典，从字典取值出来
    :param expr: 查找用的正则表达式
    return content： 替换表达式后的字符串
    """
    for ctt in re.findall(expr, content):   #匹配当前接口入参中所有的正则字符串
        content = content.replace(f'&{ctt}&', str(extractor(data, ctt)))    #将
    # 解决运算问题，实现+ -等常规数学运算， 用例书写格式{"uid":eval`&$.pid&+1`}
    for e in re.findall('eval`(.*)`', content):
        content = content.replace(f'eval`{e}`', str(eval(e)))
    #解决account加密字段处理
    for e in re.findall('base64`(.*)`', content):
        content = content.replace(f'base64`{e}`', str(base64.b64encode(e.encode("utf-8")))[2:-1])
    # 解决接口需要传uuid的问题
    for s in re.findall('UUID', content):
        content = content.replace(f'UUID',str(uuid.uuid1()))
    for t in re.findall('s_time', content):
        content = content.replace(f's_time',str(int(time.time())))
    for t1 in re.findall('e_time', content):
        content = content.replace(f'e_time',str(int(time.time()+3000)))
    return content

# {
#     "trans_id":"&$.test_002.trans_id&",
#     "access_token":"&$.test_003..datas[0].access_token&",
#     "cid":"&$.test_002..datas[0].cid&",
#     "client_ver":"3.1.0",
#     "dev_type":"7",
#     "operator_uid":"eval`&$.test_002..datas[0].cid&+1`"
# }


def convert_json(dict_str: str) -> dict:
    """
    :param dict_str: 长得像字典的字符串
    return json格式的内容
    """
    try:
        if 'None' in dict_str:
            dict_str = dict_str.replace('None', 'null')
        elif 'True' in dict_str:
            dict_str = dict_str.replace('True', 'true')
        elif 'False' in dict_str:
            dict_str = dict_str.replace('False', 'false')
        dict_str = json.loads(dict_str)
    except Exception as e:
        if 'null' in dict_str:
            dict_str = dict_str.replace('null', 'None')
        elif 'true' in dict_str:
            dict_str = dict_str.replace('true', 'True')
        elif 'False' in dict_str:
            dict_str = dict_str.replace('false', 'False')
        dict_str = eval(dict_str)
        logger.error(e)
    return dict_str


'''
写allure报告
'''
def allure_title(title: str) -> None:
    """allure中显示的用例标题"""
    allure.dynamic.title(title)

def allure_step(step: str, var: str) -> None:
    """
    :param step: 步骤及附件名称
    :param var: 附件内容
    """
    with allure.step(step):
        allure.attach(json.dumps(var, ensure_ascii=False, indent=4), step, allure.attachment_type.TEXT)