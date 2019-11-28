# encoding=utf-8
__author__ = 'lqq'
# 查找导航模块
import logging
import time

from util import readConfig, focusMove, locateElement
from util.const import Const


class Navigation(object):
    """
    循环遍历导航,返回导航名称列表
    """

    def __init__(self,navigation_info_dict):
        """
        初始化时读取配置文件，获取导航信息，导航信息为字典格式
        self.navigation_info_dict = {'first_class_navigation': 'ZWYTEST', 'second_class_navigation': ''}
        """
        self.navigation_info_dict = navigation_info_dict
        print(self.navigation_info_dict)
        logging.info(self.navigation_info_dict)

    def __get_navigation_class_xpath(self):
        """
        根据配置文件信息获取需要的导航名称对应的xpath列表NavigationName_xpath_List
        存在二级导航：[{'cctv+':'First_Navigation_Xpath1'},{'cctv5':'First_Navigation_Xpath1'}]
        不存在二级导航：[{'ZWYTEST': '//android.support.v7.widget.RecyclerView[@index=2]/android.widget.FrameLayout[@index=2]/android.widget.TextView'}]
        无导航数据：[]
        :return: NavigationName_xpath_List  导航列表
        lqq
        """
        navigation_name_xpath_list = []
        for key, value in self.navigation_info_dict.items():
            logging.info(key, value)
            nav_name_dict = {}  # 导航名称对应xpath的字典，格式：{'cctv+':['First_Navigation_Xpath1']}
            try:
                if key == 'first_class_navigation' and value != '':
                    first_navigation_xpath = Const.first_class_xpath
                    value_first_navigation = value
                    logging.info("Value_First_Navigation:", value_first_navigation)
                    nav_name_dict[value_first_navigation] = first_navigation_xpath
                    navigation_name_xpath_list.append(nav_name_dict)

                elif key == 'second_class_navigation' and value != '':
                    second_navigation_xpath = Const.second_class_xpath
                    value_second_navigation = value
                    logging.info("Value_Second_Navigation:", value_second_navigation)
                    nav_name_dict[value_second_navigation] = second_navigation_xpath
                    navigation_name_xpath_list.append(nav_name_dict)

                elif key == 'first_class_navigation' and value == '':
                    logging.error("一级导航数据不能为空")
                    break

                elif key == 'second_class_navigation' and value == '':
                    logging.info('无二级导航')
                else:
                    logging.error("导航数据错误")
                    break
            except Exception as e:
                print(e)
                logging.error(e)
        return navigation_name_xpath_list

    def __assert_target_navigation_len(self):
        """
        验证导航对应xpath的列表是否为空，如果为空直接退出程序
        不为空，返回导航对应的xpath列表及列表长度
        :return: (NavigationName_xpath_List,LenNavigationName_xpath_List)元组
        lqq
        """
        navigation_name_xpath_list = self.__get_navigation_class_xpath()
        len_navigation_name_xpath_list = len(navigation_name_xpath_list)
        try:
            if len_navigation_name_xpath_list == 0:
                logging.error("导航信息为空")
                quit()
            else:
                return navigation_name_xpath_list, len_navigation_name_xpath_list
        except Exception as e:
            print(e)

    def __find_target_navigation(self, driver):
        """
        导航信息不为空时，移动导航焦点找到目标导航
        :param driver:
        :return: 目标导航列表
        """
        navigation_name_xpath_list, len_navigation_name_xpath_list = self.__assert_target_navigation_len()
        navigation_name_list = []
        for i in range(len_navigation_name_xpath_list):
            print(navigation_name_xpath_list[i].keys())
            if len(navigation_name_xpath_list[i].keys()) != 1:
                logging.error("目标导航数据错误")
                quit()
            else:
                for key, value in navigation_name_xpath_list[i].items():
                    print(key, value, i)
                    logging.info('xpath列表:', value)
                    n = 0
                    while n <= Const.navigation_count:
                        logging.info("导航焦点右移循环次数共20次，当前次数为：%s次" % n)
                        try:
                            navigation_name = locateElement.find_element(driver, value)
                            logging.info(navigation_name.text)
                            logging.info("导航名称:", navigation_name.text)
                            if navigation_name.text == key:
                                navigation_name_list.append(navigation_name.text)
                                if i == 0:
                                    class_name = chr(i+19968)
                                else:
                                    class_name = chr(i+20107)
                                logging.info("找到了%s级导航%s" % (class_name, navigation_name.text))
                                print("找到了%s级导航%s" % (class_name, navigation_name.text))
                                break
                            else:
                                # 未找到要找的导航名称时右移一次焦点
                                focusMove.move_direction(driver, 1, 22)
                            n += 1
                        except Exception as e:
                            if n == 20:
                                logging.info('未定位到导航，已到最大循环次数%s，退出'%n)
                                quit()
                            else:
                                logging.info('未定位到导航，右移焦点')
                                focusMove.move_direction(driver, 1, 22)
                                n += 1
                                print(e)
                    # 需要增加循环等待，页面有内容时下移焦点
                    time.sleep(Const.navigation_wait_time)
                    #判断导航页有无区块
                    locateElement.element_id(driver,Const.id,n)

                    # 找到要测试的导航时，下移一次焦点
                    focusMove.move_direction(driver, 1, 20)
        # 返回要测试的导航名称列表
        return navigation_name_list

    def get_navigation_name(self, driver):
        """
        判断目标导航列表是否为空，如果为空退出程序
        目标导航不为空，返回目标导航列表
        :param driver:
        :return: 导航列表
        """
        navigation_name_list = self.__find_target_navigation(driver)
        len_navigation_name_list = len(navigation_name_list)
        try:
            if len_navigation_name_list == 0:
                logging.error("目标导航添加失败")
                quit()
            elif len_navigation_name_list == 1:
                navigation_name_list.append('')
        except Exception as e:
            logging.error(e)

        return navigation_name_list
