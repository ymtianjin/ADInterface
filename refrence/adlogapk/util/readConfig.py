# encoding=utf-8

__author__ = 'lqq'
# 读取配置文件
import os
import configparser


def read_config(section):

    """
     读取配置文件newtv.ini,将配置文件信息写成list返回
    """

    # print(os.path.dirname(os.path.abspath('.')))
    root_dir = os.path.dirname(os.path.abspath('.'))  # 获取配置文件所在上级目录

    # config = configparser.ConfigParser()
    config = MyConfigParser()
    config.read(root_dir+"/newtv.ini", encoding='UTF-8')  # 读取配置文件

    config_info = config.items(section)  # 获取指定section下的所有键值对，返回list，每个list元素为键值对元组
    return dict(config_info)


class MyConfigParser(configparser.ConfigParser):
    """
    继承configparser类，对类进行重写(调用原始类，读取配置文件，key全部变为小写)Design by lqq
    """
    def optionxform(self, optionstr):
        return optionstr
