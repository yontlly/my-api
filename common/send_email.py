import yagmail
from common import logger


def send_email(setting):
    """
    入参一个字典
    :param user: 发件人邮箱
    :param password: 邮箱授权码
    :param host: 发件人使用的邮箱服务 例如：smtp.163.com
    :param contents: 内容
    :param addressees: 收件人列表
    :param title: 邮件标题
    :param enclosures: 附件列表
    :return:
    """
    yag = yagmail.SMTP(setting['user'], setting['password'], setting['host'])
    # 发送邮件
    yag.send(setting['addressees'], setting['title'], setting['contents'])
    # 关闭服务
    yag.close()
    logger.info("邮件发送成功！")