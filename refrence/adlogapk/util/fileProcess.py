# encoding=utf-8

__author__ = 'zhangwy'

import datetime
import os


def get_file_dir(file_name):
    """
    获取文件存储路径
    :return:文件存储路径
    """
    date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    file_path = get_target_dir() + file_name + '-' + date
    return file_path


def get_target_dir():
    """
    获取日志存储上层路径
    :return:日志存储上层目标文件夹
    """
    target_dir = 'D:\\Temp'
    date = datetime.datetime.now().strftime('%Y%m%d')
    target_path = target_dir + '\\' + date + '\\'
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    else:
        print("文件夹已存在")
    return target_path


def write_txt_file(new_str, file_path):
    """
    将预期结果写入txt文件
    :param new_str: 需要写入的内容
    :param file_path:txt文件路径
    :return:
    """
    file_in = new_str+'\n'  # 需要写入的数据
    fp = open(file_path, 'a')  # 打开文件
    fp.write(file_in)  # 写入数据
    fp.flush()  # 刷新缓存
    os.fsync(fp)  # 确保文件写入磁盘
    fp.close()  # 关闭文件


def time_convert(location):
    """

    :param location:位置信息
    :return:将时分秒转化为毫秒返回
    """
    h, m, s = location.strip().split(":")
    location_convert = int(h)*3600000+int(m)*60000+int(s)*1000
    return str(location_convert)



