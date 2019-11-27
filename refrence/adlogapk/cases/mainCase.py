__author__ = 'qq'
# encoding = utf-8
import datetime
import logging,unittest
from cases import navigateAndLocation
from channel import pageTravelEntry
# from interface import interfaceEntry
from log import behaviorLog, programLog
from util import readConfig, locateElement,fileProcess
from util.const import Const


def main_case(self):
    """
    运行导航、遍历推荐位方法，执行测试用例
    :return:
    # lqq
    """
    # 判断应用是否正常启动（启动成功后，页面左上角显示央视影音logo，可能无法适配所有央视影音终端）
    try:
        locateElement.find_element(self.driver, Const.logo_xpath)
    except Exception as e:
        self.driver.quit()
        print(e)

    # 处理接口数据存储的文件
    # navigation_info_dict,page_block_list_info = interfaceEntry.interface_data_processing(file_path = 'interfaceData')
    navigation_info_dict,page_block_list_info = fileProcess.interface_data_processing(file_path = 'interfaceData')


    # 调用导航方法，移动焦点到指定页面
    navigate = navigateAndLocation.Navigation(navigation_info_dict)
    navigation_name_list = navigate.get_navigation_name(self.driver)
    logging.info(navigation_name_list)

    # 根据目标导航遍历页面区块及推荐位

    pageTravelEntry.page_block_traversal(self.driver,navigation_name_list,page_block_list_info)