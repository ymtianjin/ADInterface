# encoding=utf-8
__author__ = 'lqq'
# 程序入口
# 针对央视影音测试版本，接口数据将页面区块写错的话，终端ui自动化不具备辨识能力
# 仅支持一个区块里一个

import datetime
import logging,unittest
from cases import navigateAndLocation,mainCase
from channel import pageTravelEntry
# from interface import interfaceEntry
from log import behaviorLog, programLog
from util import readConfig, locateElement,fileProcess
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

        # 初始化Appium，启动应用
        behaviorLog.init_device(self, **devices)

        # 初始化,记录程序运行过程
        logger = logging.getLogger('start')
        logger.setLevel(logging.DEBUG)
        programLog.create_pro_log(Const.pro_log_file_path)
        # 记录运行用例
        logger.info('begin to generate testcase')
        logger.info('用例开始运行时间：' + str(datetime.datetime.now()))

    def testCase(self):
        mainCase.main_case(self)# 读取接口、验证接口数据、查找导航、遍历区块、推荐位、进入详情页




    def tearDown(self):
        """
        结束log打印，退出adb，结束Appium线程
        :return:
        """
        logging.info('用例结束运行时间为：' + str(datetime.datetime.now()))
        self.driver.quit()



if __name__ == '__main__':
    unittest.main()
