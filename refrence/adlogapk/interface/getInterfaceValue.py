# encoding=utf-8

from log import programLog

__author__ = 'chenhb'

import urllib.request
import json
import jsonpath
import logging

from util import readConfig
from util.const import Const

content_type_dict = {}
json_dict = {}
cell_code_dict = {}
tv_json_dict = {}
cell_sum = {'sum': '0'}


def index_page(url):
    """
    # 根据url返回接口数据
    :param url:接口的url
    :return unicode_str:接口的json数据
    """
    unicode_str = ''
    try:
        print(url)
        logging.info(url)
        request = urllib.request.Request(url, headers=Const.request_header)
        # request.get_method = lambda : 'HEAD'
        response = urllib.request.urlopen(request)
        # 取出json文件里的内容，返回的格式是字符串
        html = response.read()
        # 把json形式的字符串转换成python形式的Unicode字符串
        unicode_str = json.loads(html.decode('utf-8'))
    except BaseException as e:
        logging.error(e)
        unicode_str = ''
    finally:
        logging.info(url)
        return unicode_str


def get_url_value(_dict, _url):
    """
    获取url的接口数据，查询符合数据字典中的key数据，将value写回到数据字典中
    :param _dict: _dict数据字典,无value数据
    :param _url: 接口的url
    :return json_dict,unicode_str: _dict数据字典,包含value数据;接口url的json数据
    """
    try:
        unicode_str = index_page(_url)
        if unicode_str:
            for c_dirt in _dict:
                json_list = jsonpath.jsonpath(unicode_str, "$.." + c_dirt)
                json_dict[c_dirt] = json_list
        return json_dict, unicode_str
    except BaseException as e:
        programLog.error_log(e)


def get_json_str_dict_value(_json_str):
    """
    在json数据_json_str中，查询包含playStartTime、playEndTime的数据并返回
    :param _json_str:json数据
    :return:开始时间，结束时间
    """
    try:
        if _json_str:
            playStartTime = jsonpath.jsonpath(_json_str, "$..liveParam[*].playStartTime")
            playEndTime = jsonpath.jsonpath(_json_str, "$..liveParam[*].playEndTime")
        return ''.join(playStartTime), ''.join(playEndTime)
    except BaseException as e:
        programLog.error_log(e)


def get_url_block_id_value(_dict, _unicode_block_id, _block_id):
    """
    在_unicode_block_id的页面信息json数据中，查询blockId等于_block_id的某个区块的json数据，
    在某个区块的json数据中，查询数据字典_dict中的key数据，将value写回到数据字典中
    :param _dict: 数据字典
    :param _unicode_block_id: 页面信息json数据
    :param _block_id: 区块id
    :return cell_code_dict: 推荐位数据字典
    """
    try:
        block_id_list = jsonpath.jsonpath(_unicode_block_id, '$.data[?(@.blockId==' + str(_block_id) + ')]')
        if block_id_list:
            for c_dirt in _dict:
                cell_code_list = jsonpath.jsonpath(block_id_list, "$.." + c_dirt)
                cell_code_dict[c_dirt] = cell_code_list
        return cell_code_dict
    except BaseException as e:
        programLog.error_log(e)


def get_content_type_flag(content_type):
    """
    查询内容类型是否在初始化的列表中，如果存在返回True,否则返回False
    :param content_type: 内容类型
    :return: 返回True或False
    """
    try:
        conf_dict = readConfig.read_config('Json-Init')
        if content_type:
            for c_content_type in conf_dict.get('init_content_type_list').split(','):
                if c_content_type == "KD" or c_content_type == "JH":
                    c_content_type = "PS"
                if content_type == c_content_type:
                    content_type_flag = True
                    break
                else:
                    content_type_flag = False
        return content_type_flag
    except BaseException as e:
        programLog.error_log(e)


def get_content_type_value(content_type):
    """
    获取该内容类型输出的次数
    根据content_type，并返回contentType对应的value
    如果未找到符合条件的数据，自动增加contentType_dict[contentType]=contentType_value
    :param content_type: 内容类型
    :return content_type_value:内容类型值
    """
    try:
        content_type_value = ""
        content_type_flag = False
        conf_dict = readConfig.read_config('Json-Init')
        # 循环判断内容类型content_type是否在数据字典中
        # 如果存在，将内容类型值values赋值给content_type_value
        for keys, values in content_type_dict.items():
            if content_type == keys:
                content_type_value = values
                content_type_flag = True
        if not content_type_flag:
            # 循环判断内容类型content_type是否在初始化的内容类型列表中
            # 如果存在,将会把此类型添加到数据字典中，即content_type_dict[content_type] = '0'
            # 如果不存在，给出提示信息
            for init_content_type in conf_dict.get('init_content_type_list').split(','):
                if content_type == init_content_type:
                    content_type_value = '0'
                    content_type_dict[content_type] = content_type_value
                    logging.info('添加内容类型[%s=%s]' % (content_type, content_type_value))
                    print("添加内容类型[%s=%s]" % (content_type, content_type_value))
                    break
                else:
                    logging.info("初始化内容类型列表中不包括[%s]" % content_type)
                    print("初始化内容类型列表中不包括[%s]" % content_type)
        else:
            logging.info('获取内容类型[%s=%s]' % (content_type, content_type_value))
            print("获取内容类型[%s=%s]" % (content_type, content_type_value))
        return content_type_value
    except BaseException as e:
        programLog.error_log(e)


def check_content_type_value():
    """
    判断初始化内容类型列表中init_content_type_list的类型个数与数据字典的长度是否相等，
    如果相等，循环判断数据字典中的values与初始化中内容类型个数init_content_type_sum是否相等，
              如果相等则check_sum加1；
              循环结束后，如果check_sum等于数据字典长度，check_flag = True；否则check_flag = False
    :return check_flag:所有内容类型输出状态
    """
    try:
        check_sum = 0
        check_flag = False
        conf_dict = readConfig.read_config('Json-Init')
        if len(conf_dict.get('init_content_type_list').split(',')) == len(content_type_dict):
            for keys, values in content_type_dict.items():
                if int(conf_dict.get('init_content_type_sum')) == int(values):
                    check_sum += 1
            if len(content_type_dict) == check_sum:
                check_flag = True
            else:
                check_flag = False
        return check_flag
    except BaseException as e:
        programLog.error_log(e)


def get_content_type_not_vip_flag(content_type):
    """
    在初始化没有vip标识列表中，查询content_type是否在列表中，如果存在则将vip_flag赋值'0'
    :param content_type:内容类型
    :return: 返回免费标识'0'
    """
    try:
        # TV,FG节目没有vip标识
        vip_flag = ["null"]
        conf_dict = readConfig.read_config('Json-Init')
        for c_content_type in conf_dict.get('init_content_type_not_vip_flag').split(','):
            if c_content_type == content_type:
                vip_flag = '0'
        return vip_flag
    except BaseException as e:
        programLog.error_log(e)


def init_content_type_dict():
    try:
        content_type_dict.clear()
    except BaseException as e:
        programLog.error_log(e)


def set_cell_sum():
    try:
        cell_sum['sum'] = int(cell_sum['sum']) + 1
    except BaseException as e:
        programLog.error_log(e)


def get_cell_sum():
    try:
        if cell_sum['sum']:
            _cell_sum = cell_sum['sum']
        else:
            _cell_sum = '0'
        cell_sum['sum'] = '0'
        return _cell_sum
    except BaseException as e:
        programLog.error_log(e)



