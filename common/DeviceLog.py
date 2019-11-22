# encoding=utf-8
__author__ = 'limeng'

import os
from selenium.webdriver.common.keys import Keys

class DeviceLog:
    def __init__(self):
        pass

    def connect(self, device_ip, device_name):
        for i in range(10):
            try:
                execute_cmd = os.popen('adb devices')
                cmd_result = execute_cmd.readlines()
                if len(cmd_result) == 3:
                    device_info = (cmd_result[1].strip()).split()
                    # print device_name
                    if device_info[1] == 'device' and device_info[0] == device_name:
                        print("设备已连接,设备名称为" + device_name)
                        break
                    elif device_info[1] == 'offline':
                        raise Exception("设备掉线，请检查后重新连接")
                    else:
                        raise Exception("未连接到指定设备")
                elif len(cmd_result) == 1:
                    print("设备连接异常，需要重新进行连接")
                    os.popen('adb connect ' + device_ip)  # 使用adb connect命令进行连接
                    continue
                else:
                    raise Exception("设备无法连接，请检查")
            except Exception as e:
                print(e)
                break

    def disconnect(self):
        """
            结束打印日志,关闭adb服务
            """
        os.popen(Keys.CONTROL + 'c')
        # os.popen('ctrl+c')
        os.popen('adb kill-server')

    def clear_cache(self, app_package):
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

    def log_start(self, log_file_path):
        """
        开始打印日志
        """
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
        else:
            print("开始打印log")
            os.popen('adb logcat -v time >' + log_file_path)
            # os.popen('adb logcat -c')
            # # log_file = open(log_file_path, 'w')
            # log_cmd = 'adb logcat -v time >'+log_file_path
            # pop_log = subprocess.Popen(log_cmd, shell=True)
            # # pop_log = subprocess.Popen(log_cmd, stdout=log_file_path, stderr=subprocess.PIPE)
            # return pop_log