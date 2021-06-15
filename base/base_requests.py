import requests
from common import allure_step, allure_title, logger, extractor, rep_expr
from common.data_process import DataProcess
from common.read_file import ReadFile
import allure


class BaseRequest(object):
    session = None

    @classmethod
    def get_session(cls):
        if cls.session is None:
            cls.session = requests.Session()
        return cls.session

    @classmethod
    def send_request(cls, case: list, env: str = 'dev') -> object:
        """处理case数据，转换成可用数据发送请求
        :param case: 读取出来的每一行用例内容，可进行解包
        :param env: 环境名称 默认使用config.yaml server下的 dev 后面的基准地址
        return: 响应结果， 预期结果
        """
        case_number,  case_feature, case_step ,case_title, path, token, method, parametric_key, file_obj, data, sql, response,expect = case
        # allure报告 用例标题
        allure_title(case_title)
        # allure_step(case_step)
        # allure.dynamic.feature(case_feature)
        # allure.dynamic.story(case_step)
        # allure.dynamic.title(case_title)
        # 处理url、header、data、file、的前置方法
        test = "test"
        pwd = "pwd"
        if test in case_number:
            url1 = ReadFile.read_config(
                f'$.server.{env}') + DataProcess.handle_path(path)
            url = url1.replace("8888", "8787")
        elif pwd in case_number:
            url1 = ReadFile.read_config(
                f'$.server.{env}') + DataProcess.handle_path(path)
            url = url1.replace("8888", "8282")
        else:
            url = ReadFile.read_config(
                f'$.server.{env}') + DataProcess.handle_path(path)
        allure_step('请求地址', url)

        header = DataProcess.handle_header(token)
        allure_step('请求头', header)

        data = DataProcess.handle_data(data)
        allure_step('请求参数', data)

        file = DataProcess.handler_files(file_obj)
        allure_step('上传文件', file_obj)

        # 发送请求
        res = cls.send_api(url, method, parametric_key, header, data, file)
        allure_step('响应耗时(s)', res.elapsed.total_seconds())
        allure_step('响应内容', res.json())

        # 响应后操作
        if token == '写':
            DataProcess.have_token['Authorization'] = extractor(res.json(), ReadFile.read_config('$.expr.token'))
            allure_step('请求头中添加Token', DataProcess.have_token)

        '''
        构建数据池，用以数据关联是调用之前接口回参
        '''
        DataProcess.save_response(case_number, res.json())
        allure_step('存储实际响应', DataProcess.response_dict)

        return res.json(), expect, sql

    @classmethod
    def send_api(cls, url, method, parametric_key, header=None, data=None, file=None) -> object:
        """
        :param method: 请求方法
        :param url: 请求url
        :param parametric_key: 入参关键字， get/delete/head/options/请求使用params,
         post/put/patch请求可使用json（application/json）/data
        :param data: 参数数据，默认等于None
        :param file: 文件对象
        :param header: 请求头
        :return: 返回res对象
        """
        session = cls.get_session()

        if parametric_key == 'params':
            res = session.request(method=method, url=url, params=data, headers=header)
        elif parametric_key == 'data':
            res = session.request(method=method, url=url, data=data, files=file, headers=header)
        elif parametric_key == 'json':
            res = session.request(method=method, url=url, json=data, files=file, headers=header)
        else:
            raise ValueError(
                '可选关键字为：get/delete/head/options/请求使用params, post/put/patch请求可使用json（application/json）/data')
        logger.info(f'\n最终请求地址:{res.url}\n请求方法:{method}\n请求头:{header}\n请求参数:{data}\n上传文件:{file}\n响应数据:{res.json()}')
        return res