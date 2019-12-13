# encoding=utf-8
__author__ = 'limeng'

import os, json, time, logging
from selenium.webdriver.common.keys import Keys

class DeviceLog:
    def __init__(self, param):
        self.device_ip = param.__contains__("global_device_ip") and param["global_device_ip"] or ""
        self.device_name = param.__contains__("global_device_name") and param["global_device_name"] or ""
        self.app_package = param.__contains__("global_app_package") and param["global_app_package"] or ""
        self.sdk_name = param.__contains__("global_sdk_name") and param["global_sdk_name"] or ""
        pass

        #连接设备
    def connect(self):
        for i in range(10):
            try:
                execute_cmd = os.popen('adb devices')
                cmd_result = execute_cmd.readlines()
                if len(cmd_result) == 3:
                    device_info = (cmd_result[1].strip()).split()
                    # print device_name
                    if device_info[1] == 'device' and device_info[0] == self.device_name:
                        print("设备已连接,设备名称为" + self.device_name)
                        break
                    elif device_info[1] == 'offline':
                        raise Exception("设备掉线，请检查后重新连接")
                    else:
                        raise Exception("未连接到指定设备")
                elif len(cmd_result) == 1:
                    print("设备连接异常，需要重新进行连接")
                    os.popen('adb connect ' + self.device_ip)  # 使用adb connect命令进行连接
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

    def clear_cache(self):
        """
        清除应用缓存
         :param    app_package   apk包名
        """
        for i in range(10):
            try:
                clear_cache_cmd = os.popen('adb shell pm clear ' + self.app_package)
                clear_cache_result = clear_cache_cmd.readline().strip()
                if clear_cache_result == 'Success':
                    print("清理缓存成功")
                    break
                time.sleep(2)
            except Exception as e:
                print(e)
                break

    def log_start(self, log_file_path):
        """
        开始打印日志
        """
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
        else:
            print("开始打印log")
            os.popen("adb -s " + self.device_name + " logcat -v time *:s " + self.sdk_name + " > " + log_file_path)
            # os.popen('adb logcat -c')
            # # log_file = open(log_file_path, 'w')
            # log_cmd = 'adb logcat -v time >'+log_file_path
            # pop_log = subprocess.Popen(log_cmd, shell=True)
            # # pop_log = subprocess.Popen(log_cmd, stdout=log_file_path, stderr=subprocess.PIPE)
            # return pop_log

    #从日志中提取需要的数据
    def __check_ad_data(self, request, checkResult, adResult):
        try:
            data = json.loads(request)
            if not isinstance(data, dict) or not data.__contains__("adspaces"):
                return
            adSpaces = data["adspaces"]
            for type, adData in adSpaces.items():
                if not isinstance(adData, list) or len(adData) == 0:
                    continue
                for ad in adData:
                    if not isinstance(ad, dict):
                        continue
                    for check, value in checkResult.items():
                        if not ad.__contains__(check):
                            continue
                        if not adResult.__contains__(check):
                            adResult[check] = [ad[check]]
                        else:
                            adResult[check].append(ad[check])
        except Exception as e:
            logging.info(e)

    #判断设备中的期望值
    def log_read(self, log_file_path, checkResult):
        try:
            missionMids = []
            file = open(log_file_path, mode="rb")
            content = str(file.read())
            lines = content.split("\\r\\n")
            adResult = {}
            for line in lines:
                line = line.strip()
                if not isinstance(line, str) or len(line) < 130:
                    continue
                start = line.find("{\"adspaces\":")
                end = line.rfind("}")
                if start < 0 or end < 0 or start > end:
                    continue
                request = line[start:end + 1].strip()
                request = request.replace("\\\\\"", "\"")
                request = request.replace("\"{", "{")
                request = request.replace("}\"", "}")
                request = request.replace("\\x", "x")
                self.__check_ad_data(request, checkResult, adResult)
            for type, value in checkResult.items():
                if not adResult.__contains__(type): # 说明期望的广告在日志中没有读到
                    missionMids.append(type + "：" + str(value) + "：node mission")
                else:
                    result = adResult[type]
                    if isinstance(value, list) and len(value) > 0:
                        for v in value:
                            if v not in result:
                                missionMids.append(type + "：" + str(v) + "：value dismatch")
                    elif isinstance(value, str) or isinstance(value, int):
                        if str(value) != str(result[-1]):
                            missionMids.append(type + "：" + str(value) + "：value dismatch")
            return missionMids
        except Exception as e:
            logging.info(e)
        return []