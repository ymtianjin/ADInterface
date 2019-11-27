# encoding=utf-8
# @author:chenhaibin

import logging

from interface import getInterfaceValue
from log import programLog
from util.const import Const


def query_content(content_id, content_type):
    """
    # content_id长度大于3才会调用方法query_content_title_vip_series_type去查询内容标题、vip标识、内容类型
    :param content_id:内容id
    :param content_type:内容类型
    :return c_content_title, c_vip_flag, c_content_type:内容标题；内容vip标识；内容类型
    """
    try:
        c_content_title = ""
        c_vip_flag = ""
        c_content_type = ""
        if 3 < len(content_id):
            new_content_id = content_id[:2] + '/' + content_id[-2:] + '/' + content_id
            c_content_title, c_vip_flag, c_content_type = query_content_title_vip_series_type(new_content_id, content_type)
        else:
            print(u"content_id=%s的长度小于3位数" % content_id)
        return c_content_title, c_vip_flag, c_content_type
    except BaseException as e:
        programLog.error_log(e)


def query_content_title_vip_series_type(content_id, content_type):
    """
    # 在节目集接口中，查询vipFlag,seriesType,获取vipFlag等于0的数据中，细化seriesType的内容类型
    # 获取免费节目,vipFlag取值定义：未设置 ：-1,免费：0,会员单点：1,会员VIP：3,单点：4
    # PS节目集下的细分，seriesType为0时，代表是看点形式(KD)，即详情页显示图片；为1时，是剧集形式(JH)，即详情页显示集号
    :param content_id:内容id
    :return c_content_title, c_vip_flag, c_content_type:内容标题；内容vip标识；内容类型
    """
    try:
        content_dirt = {'title': '', 'vipFlag': '', 'seriesType': ''}
        url_content = Const.url_content + content_id + '.json'
        content_dirt, json_value = getInterfaceValue.get_url_value(content_dirt, url_content)
        vip_flag_arr = content_dirt['vipFlag']
        content_title_arr = content_dirt['title']
        series_type_arr = content_dirt['seriesType']

        if not content_title_arr:
            c_content_title = ['null']
        else:
            c_content_title = content_title_arr[0]
        print('标题=%s' % c_content_title)
        logging.info("标题=%s" % c_content_title)
        if not series_type_arr:
            c_content_type = ['null']
        else:
            c_content_type = series_type_arr[0]
        if not vip_flag_arr:
            vip_flag = getInterfaceValue.get_content_type_not_vip_flag(content_type)
            c_vip_flag = vip_flag
        else:
            c_vip_flag = vip_flag_arr[0]
        if content_title_arr and series_type_arr and vip_flag_arr:
            for index_vip_flag in range(len(vip_flag_arr)):
                if not content_title_arr[index_vip_flag]:
                    continue
                if '0' == vip_flag_arr[index_vip_flag]:
                    c_vip_flag = str(vip_flag_arr[index_vip_flag])
                    c_content_title = content_title_arr[index_vip_flag]
                    if '0' == series_type_arr[index_vip_flag]:
                        c_content_type = 'KD'
                    elif '1' == series_type_arr[index_vip_flag]:
                        c_content_type = 'JH'
                else:
                    c_vip_flag = vip_flag_arr[0]
                    c_content_title = content_title_arr[0]
                    c_content_type = series_type_arr[0]
        return c_content_title, c_vip_flag, c_content_type
    except BaseException as e:
        programLog.error_log(e)
