# encoding=utf-8
import logging

__author__ = 'lqq'
# 进入详情页后退出

import os
import time
# from cases import detailAndClick
from util import fileProcess, readConfig, focusMove, locateElement
from util.const import Const




# def verify(driver, content_type, content_name):
def verify(driver,block_recommend_no,content_num):
    """
    点击确认键，进入详情页，判断视频是否正常起播
    :param driver:用例驱动
    # :param content_type:节目类型
    # :param  content_name :详情页标题
    :return:
    """
    try:
        list_page_attr = driver.current_activity  # 获取导航页页面属性
        logging.info('testCase:' + '获取导航页页面属性'+list_page_attr)
        time.sleep(2)

        print('点击确认键进入详情页')
        focusMove.move_direction(driver, 1, 23)  # 点击确认按钮，进入详情页
        logging.info('testCase:'+'点击确认按钮，进入详情页')
        time.sleep(8)
        detail_page_attr = driver.current_activity  # 获取详情页页面属性
        logging.info('testCase:' + '获取详情页页面属性' + detail_page_attr)

        if list_page_attr != detail_page_attr:
            detail_title_name = driver.find_element_by_id(Const.detail_title_id).text
            logging.info('testCase:' + '获取详情页标题' + detail_title_name)

            # # 推荐位内容写回-----
            # fileProcess.interface_data_return(detail_title_name)

            # 进入详情页成功，判断视频是否正常播放(是否存在错误码和播放鉴权失败提示)
            elements = [Const.err_code_xpath, Const.err_auth_xpath]
            err_name_text = locateElement.elements_exist(driver, elements)
            print(err_name_text)
            logging.info('testCase:' + '错误码' + err_name_text)
            if err_name_text != '' and (u'失败' or u'错误' in err_name_text):

                # 视频播放失败，点击返回按钮，退出详情页
                logging.error('testCase' + '视频播放失败,节目详情页标题为#' + detail_title_name)

                # 推荐位内容写回-----
                Flag = False
                # fileProcess.interface_data_return(block_recommend_no,content_num,detail_title_name,Flag)
                fileProcess.interface_data_return(Flag)
                focusMove.move_direction(driver, 1, 4)  # 点击返回按钮，返回导航页

            else:
                # 视频正常播放
                logging.info('testCase:' + '视频正常播放，开始执行测试用例')
                time.sleep(15)

                # 推荐位内容写回-----
                Flag = True
                # fileProcess.interface_data_return(block_recommend_no,content_num,detail_title_name,Flag)
                fileProcess.interface_data_return(Flag)
                focusMove.move_direction(driver, 1, 4)  # 点击返回按钮，返回导航页

        else:
            logging.error('testCase' + '无法进入详情页，第' + content_num + '个推荐位')
            # 推荐位内容写回-----
            Flag = False
            # fileProcess.interface_data_return(block_recommend_no,content_num,Flag)
            fileProcess.interface_data_return(Flag)
    except Exception as e:
        print(e)

