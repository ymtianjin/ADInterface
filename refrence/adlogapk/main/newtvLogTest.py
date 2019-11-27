# encoding=utf-8
import datetime

__author__ = 'zhangwy'
import logging
import unittest

from cases import navigateAndLocation
from channel import pageTravelEntry
from log import behaviorLog, programLog
from log.behaviorLog import log_exit
from util import readConfig, locateElement
from util.const import Const


class NewTVLogTest(unittest.TestCase):

    def setUp(self):

        """
        启动adb，清除应用缓存，启动初始化Appium过程
        """

        # 读取配置文件，连接指定设备，并清除被测试应用的本地缓存
        devices = readConfig.read_config("Device-Info")
        behaviorLog.adb_connect(devices.get('deviceIP'), devices.get('deviceName'))  # 启动adb，连接设备
        behaviorLog.clear_cache(devices.get('appPackage'))  # 清除应用缓存

        # 启动logcat日志打印，实时采集用户行为日志
        behaviorLog.log_start(Const.log_file_path)
        # 新建txt文件，在运行过程中生成预期结果
        open(Const.result_file_path, 'w').close()  # 新建CaseResult.txt文件（存储预期字段值）
        open(Const.except_file_path, 'w').close()  # 新建CaseExcept.txt文件（存储预期上报日志节点顺序）

        # 初始化Appium，启动应用
        behaviorLog.init_device(self, **devices)
        # start_time = datetime.datetime.now()
        # print(start_time)

        # 初始化运行日志，记录程序运行过程
        logger = logging.getLogger('start')
        logger.setLevel(logging.DEBUG)
        programLog.create_pro_log(Const.pro_log_file_path)
        # 打印日志，运行用例
        logger.info('begin to generate testcase')
        logger.info('用例开始运行时间：' + str(datetime.datetime.now()))

    def testCase(self):
        """
        运行导航、遍历推荐位方法，执行测试用例
        :return:
        """

        # 判断应用是否正常启动（启动成功后，页面左上角显示央视影音logo，可能无法适配所有央视影音终端）
        try:
            locateElement.find_element(self.driver, Const.logo_xpath)
        except Exception as e:
            self.driver.quit()
            print(e)

        # 调用导航方法，移动焦点到指定页面
        navigate = navigateAndLocation.Navigation()
        navigation_name_list = navigate.get_navigation_name(self.driver)
        print(navigation_name_list)
        logging.info(navigation_name_list)

        # 根据目标导航遍历页面区块及推荐位
        pageTravelEntry.page_block_traversal(self.driver, navigation_name_list)

    def tearDown(self):
        """
        结束log打印，退出adb，结束Appium线程
        :return:
        """
        logging.info('用例结束运行时间为：' + str(datetime.datetime.now()))
        log_exit()
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
