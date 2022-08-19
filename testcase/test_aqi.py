import pytest
from common.read_file import ReadFile

from base.base_requests import BaseRequest
from common.data_process import DataProcess


@pytest.fixture(params=ReadFile.read_testcase())
def cases(request):
    """用例数据，测试方法参数入参该方法名 cases即可，实现同样的参数化
    目前来看相较于@pytest.mark.parametrize 更简洁。
    """
    return request.param



# https://www.cnblogs.com/shouhu/p/12392917.html
# reruns 重试次数 reruns_delay 次数之间的延时设置（单位：秒）
# 失败重跑，会影响总测试时长，如不需要 将 @pytest.mark.flaky(reruns=3, reruns_delay=5) 注释即可
@pytest.mark.flaky(reruns=0, reruns_delay=1)
def test_main(cases,env_jenkins,account_jenkins):#cases, get_db
    # 此处的cases入参来自cases函数，与直接使用 @pytest.mark.parametrize有着差不多的效果
    #数据池先记录本次测试使用的基础account值
    #DataProcess.save_response('test_account',ReadFile.read_config(f'$.account.test_account'))#读取yaml文件
    DataProcess.save_response('test_account', account_jenkins)
    # 发送请求
    response, expect, sql = BaseRequest.send_request(cases,env_jenkins)
    # 执行sql
    # DataProcess.handle_sql(sql, get_db)
    # 断言操作
    DataProcess.assert_result(response, expect)