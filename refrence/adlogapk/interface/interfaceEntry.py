# encoding=utf-8
# @author:chenhaibin
import datetime
import time
import logging
import jsonpath

from log import programLog
from util.const import Const
from interface import getInterfaceValue, getQueryLayoutCode


def name_change_id(page_name):
    """
    # 在导航页接口中，根据导航名字page_name查询出id
    # 将查询出的id传给页面信息接口
    # 将页面信息传给函数query_layoutCode
    :param page_name:导航名称
    :return page_id, panel_name：导航id和导航名称
    """
    try:
        page_id = ""
        print(u'接收数据=%s' % (str(page_name)))
        logging.info('接收数据=%s' % (str(page_name)))
        if '' == page_name[1]:
            panel_name = page_name[0]
            json_check_str = "$.data[?(@.title=='" + str(page_name[0]) + "')]"
        else:
            panel_name = page_name[1]
            json_check_str = "$.data[?(@.title=='" + str(page_name[0]) + "')].child.[?(@.title=='" + str(page_name[1]) + "')]"
        print(u'页面名称=%s' % panel_name)
        logging.info('页面名称=%s' % panel_name)
        keys_dirt = {'id': '', 'title': ''}
        unicode_list = getInterfaceValue.index_page(Const.url_index)
        if 0 < len(unicode_list):
            keys_list_unicode = jsonpath.jsonpath(unicode_list, json_check_str)
            for c_keys_dirt in keys_dirt:
                keys_list = jsonpath.jsonpath(keys_list_unicode, "$.." + c_keys_dirt)
                keys_dirt[c_keys_dirt] = keys_list
            id_arr = keys_dirt['id']
            title_arr = keys_dirt['title']
            if id_arr and title_arr:
                for i in range(len(id_arr)):  # id值是唯一的，title可能存在重复的情况
                    if title_arr[i] == panel_name:
                        print(u'页面ID=%s' % (id_arr[i]))
                        logging.info('页面ID=%s' % (id_arr[i]))
                        page_id = id_arr[i]
                        break
        return page_id, panel_name
    except BaseException as e:
        programLog.error_log(e)
        pass


def get_json_value(page_name):
    """
    # 根据page_name,返回json数据
    :param page_name:导航名称
    :return json_str:返回该导航的json数据
    """
    try:
        begin_time = datetime.datetime.now()
        json_list = []
        for run_sum in range(1, 5):
            logging.info(u'运行次数：%s' % run_sum)
            print(u'运行次数：%s' % run_sum)
            page_id, panel_name = name_change_id(page_name)
            if "" != page_id:
                json_layout_value = getQueryLayoutCode.query_layout_code(panel_name, page_id)
                if '[]' != json_layout_value:
                    break
            time.sleep(3)
        end_time = datetime.datetime.now()
        layout_cell_sum = getInterfaceValue.get_cell_sum()
        print("开始时间:%s" % begin_time)
        print("结束时间:%s" % end_time)
        print("推荐位总数:%s" % layout_cell_sum)
        print("使用时间:%s秒" % (end_time-begin_time).seconds)
        logging.info('------------------------------------------------------------------------------------')
        logging.info('json_str：%s' % json_layout_value[:-1])
        logging.info('------------------------------------------------------------------------------------')
        if int(layout_cell_sum) != 0:
            return eval('[' + json_layout_value[:-1] + ']')
        else:
            return json_list
    except BaseException as e:
        programLog.error_log(e)
        return json_list
        pass
