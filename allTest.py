import os
import shutil
from testcase.test_aqi import pytest
from common import logger,dir_base
from common.read_file import ReadFile
#import logger

report = dir_base(ReadFile.read_config('$.file_path.report'))
logfile = dir_base(ReadFile.read_config('$.file_path.log'))

def run():
    if os.path.exists(dir_base('report/')):
        shutil.rmtree(path=dir_base('report/'))
    logger.add(logfile, enqueue=True, encoding='utf-8')
    logger.info('开始测试...')
    pytest.main(
        args=[
            dir_base('testcase/test_aqi.py'),
            "-s",
            "-v",
            f'--alluredir={report}/data'])
    # 自动以服务形式打开报告
    #os.system(f'allure serve {report}/data')
    # 本地生成报告
    #os.system(f'allure generate {report}/data -o {report}/html --clean')

    #docker镜像使用
    #os.system(f'allure generate {report}/data -o /usr/local/apache-tomcat-10.0.6/webapps/html --clean')

    logger.success('报告已生成')


if __name__ == '__main__':
    run()