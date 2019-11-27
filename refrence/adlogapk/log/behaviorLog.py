# encoding=utf-8
__author__ = 'lqq'
# 设备连接、清除缓存
from util import readConfig
import os
from appium import webdriver
from selenium.webdriver.common.keys import Keys


def adb_connect(device_ip, device_name):
    """
    启动adb服务，连接设备
    :param    device_ip   需要连接的设备ip
    :param    device_name   设备名称，通过adb device获得
    """

    os.popen('adb start-server')  # 启动adb服务
    times = readConfig.read_config("Device-Connect").get('connect_times')
    for i in range(int(times)):
        try:
            execute_cmd = os.popen('adb devices')
            cmd_result = execute_cmd.readlines()
            if len(cmd_result) == 3:
                device_info = (cmd_result[1].strip()).split()
                # print device_name
                if device_info[1] == 'device' and device_info[0] == device_name:
                    print("设备已连接,设备名称为"+device_name)
                    break
                elif device_info[1] == 'offline':
                    raise Exception("设备掉线，请检查后重新连接")
                else:
                    raise Exception("未连接到指定设备")
            elif len(cmd_result) == 1:
                print("设备连接异常，需要重新进行连接")
                os.popen('adb connect '+device_ip)  # 使用adb connect命令进行连接
                continue
            else:
                raise Exception("设备无法连接，请检查")
        except Exception as e:
            print(e)
            break


def clear_cache(app_package):

    """
    清除应用缓存
     :param    app_package   apk包名
    """

    try:
        while True:
            clear_cache_cmd = os.popen('adb shell pm clear ' + app_package)
            clear_cache_result = clear_cache_cmd.readline().strip()
            if clear_cache_result == 'Success':
                print("清理缓存成功")
                break
    except Exception as e:
        print(e)



def init_device(self, **devices):
    """
    读取设备配置信息，初始化appium
    :param: **devices  设备信息
    :return: 返回驱动driver
    """
    desired_caps = {

        'deviceName': devices['deviceName'],  # 设备信息，adb devices命令得到的值
        'platformName': devices['platformName'],  # 系统信息，Android/IOS
        'platformVersion': devices['platformVersion'],  # 系统版本号
        'automationName': devices['automationName'],  # Appium
        'appPackage': devices['appPackage'],  # 被测试apk包名
        'appActivity': devices['appActivity'],  # 被测试apk启动页
        'appWaitActivity': devices['appWaitActivity'],  # 填写测试包等待页
        'noReset': True,  # 不要在会话前重置应用状态
        'unicodeKeyboard': True,  # 使用 Unicode 输入法
        'resetKeyboard': True,  # Unicode 测试结束后，重置输入法到原有状态
        'newCommandTimeout': devices['newCommandTimeout'],  # 设置过期时间

    }

    self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
