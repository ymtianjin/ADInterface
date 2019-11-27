# encoding=utf-8
import logging

__author__ = 'zhangwy'
import os
import time

from cases import detailAndOperation
from util import fileProcess, readConfig, focusMove, locateElement
from util.const import Const


class ParamAndPlay(object):

    def __init__(self):

        self.flag1 = ':0'
        self.nodes = readConfig.read_config("Log-Node")

    def verify(self, driver, content_type, content_num):
        """
        点击确认键，进入详情页，判断视频是否正常起播
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:
            # flag = True
            video_flag = '#' + content_num + self.flag1
            list_page_attr = driver.current_activity  # 获取导航页页面属性
            logging.info('testCase:' + '获取导航页页面属性'+list_page_attr)
            time.sleep(2)

            print('点击确认键进入详情页')
            # driver.keyevent(23)
            focusMove.move_direction(driver, 1, 23)  # 点击确认按钮，进入详情页
            logging.info('testCase:'+'点击确认按钮，进入详情页')
            time.sleep(5)

            detail_page_attr = driver.current_activity  # 获取详情页页面属性
            logging.info('testCase:' + '获取详情页页面属性' + detail_page_attr)

            detail_title_name = driver.find_element_by_id(Const.detail_title_id).text
            logging.info('testCase:' + '获取详情页标题' + detail_title_name)

            if list_page_attr != detail_page_attr:

                # 进入详情页成功，判断视频是否正常播放(是否存在错误码和播放鉴权失败提示)
                elements = [Const.err_code_xpath, Const.err_auth_xpath]
                err_name_text = locateElement.elements_exist(driver, elements)
                print(err_name_text)
                logging.info('testCase:' + '错误码' + err_name_text)
                if err_name_text != '' and (u'失败' or u'错误' in err_name_text):

                    # 视频播放失败，点击返回按钮，退出详情页，并记录18|0日志

                    logging.error('testCase' + '视频播放失败,节目详情页标题为#' + detail_title_name)
                    focusMove.move_direction(driver, 1, 4)  # 点击返回按钮，返回导航页
                    logging.info('testCase:' + '视频播放失败，点击返回导航页')
                    fileProcess.write_txt_file(self.nodes.get('playRec') + video_flag, Const.except_file_path)

                else:
                    # 视频正常播放，读取配置文件，执行指定用例
                    logging.info('testCase:' + '视频正常播放，开始执行测试用例')
                    obj = detailAndOperation.DetailAndOperation()
                    file = os.path.dirname(os.path.abspath('.')) + "/CaseList"
                    for line in open(file):
                        method_name = line.strip().split("#")[1]
                        logging.info('testCase:' + '当前用例名称为#' + method_name)

                        if line.strip().split("#")[0] == 'DetailAndOperation':
                            getattr(obj, method_name)(driver, content_type, content_num)
                        else:
                            print('非法输入:' + line)
                            logging.info('testCase' + '当前用例不符合执行条件' + method_name)

                    open(file).close()
            else:
                print('无法进入详情页')
                logging.error('testCase' + '无法进入详情页，第' + content_num + '个推荐位')
        except Exception as e:
            print(e)

