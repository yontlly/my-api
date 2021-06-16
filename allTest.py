import os
import shutil
from testcase.test_aqi import pytest
from common import logger
from common.read_file import ReadFile
#import logger

report = ReadFile.read_config('$.file_path.report')
logfile = ReadFile.read_config('$.file_path.log')


def run():
    if os.path.exists('report/'):
        shutil.rmtree(path='report/')
    logger.add(logfile, enqueue=True, encoding='utf-8')
    logger.info('开始测试...')
    pytest.main(
        args=[
            'testcase/test_aqi.py',
            "-s",
            "-v",
            f'--alluredir={report}/data'])
    # 自动以服务形式打开报告
    os.system(f'allure serve {report}/data')
    # 本地生成报告
    os.system(f'allure generate {report}/data -o {report}/html --clean')
    logger.success('报告已生成')


if __name__ == '__main__':
    run()