import pytest


# pytest_addoption(parser) 定义自己的命令行参数的固定写法
def pytest_addoption(parser):
    # 定义 --env_opt 参数名
    parser.addoption("--env_jenkins", default="dev", help="测试环境", action="store")

    # 定义 --run_level 参数名
    # 参数说明：
    #   default：当命令行不调用参数时的默认值
    #   help：在帮助中显示的说明
    parser.addoption("--account_jenkins", default="wer", help="测试用account", action="store")


# 获取--env_opt参数值
@pytest.fixture(scope="session")
def env_jenkins(request):
    return request.config.getoption("--env_jenkins")


# 获取--run_level参数值
@pytest.fixture(scope="session")
def account_jenkins(request):
    return request.config.getoption("--account_jenkins")