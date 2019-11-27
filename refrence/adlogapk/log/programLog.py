# encoding=utf-8
import logging

__author__ = 'lqq'
# 程序运行日志



def create_pro_log(path):
    """
    创建运行日志，记录程序运行过程
    :param path: 日志存储路径
    :return: 
    """
    # 获取根日志,不指定名称，默认返回root
    log_root = logging.getLogger()
    # 设置日志级别
    log_root.setLevel(logging.DEBUG)

    # 创建filehandle，日志格式
    # 且文件的第一行是：'Time,Level,Logger Name,Message'
    log_handle_root = logging.FileHandler(path, encoding='utf-8')
    log_handle_root.setLevel(logging.DEBUG)
    log_root.addHandler(log_handle_root)
    log_root.info('Time,Level,Logger Name,Message')
    file_format = logging.Formatter("%(asctime)s %(filename)s %(funcName)s - %(message)s", "%Y-%m-%d %H:%M:%S")
    log_handle_root.setFormatter(file_format)

    # 创建streamhandle，日志格式
    log_handle = logging.StreamHandler()
    log_handle.setLevel(logging.INFO)
    stream_format = logging.Formatter("%(asctime)s %(filename)s %(funcName)s - %(message)s", "%Y-%m-%d %H:%M:%S")
    log_handle.setFormatter(stream_format)
    log_root.addHandler(log_handle)

    return log_root

