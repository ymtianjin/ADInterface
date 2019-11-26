# encoding=utf-8

__author__ = 'limeng'
from appium import webdriver
import time, logging

class Naviage:
    def __init__(self):
        # 常量定义
        self.app_tag = "com.newtv.cboxtv"
        # 页面左上角logo的xpath定位，用于判断应用是否正常启动
        self.logo_xpath = '//android.widget.RelativeLayout[@index=0]/android.widget.ImageView[@index=1]'
        # 一级导航的xpath
        self.first_class_xpath = '//android.support.v7.widget.RecyclerView[@index=2]/android.widget.FrameLayout[@index=2]/android.widget.TextView'
        # 二级导航的xpath
        self.second_class_xpath = '//android.widget.FrameLayout[@index=4]/android.widget.RelativeLayout[@index=0]' \
                             '/android.support.v7.widget.RecyclerView[@index=0]/android.widget.RelativeLayout[@index=3]/android.widget.TextView'
        # 详情页标题id，用于判断是否进入指定详情页
        self.detail_title_id = self.app_tag + ':id/id_detail_title'
        # 播放失败错误码
        self.err_code_xpath = '//android.widget.FrameLayout[@index=1]/android.widget.FrameLayout[@index=0]/android.widget.TextView[@index=0]'
        # 播放鉴权失败
        self.err_auth_xpath = '//android.widget.FrameLayout[@index=1]/android.widget.FrameLayout[@index=0]/android.widget.TextView[@index=3]'
        # 查找导航循环次数
        self.navigation_count = 20
        # 一级导航焦点下移至二级导航时的等待时长
        self.navigation_wait_time = 5

        self.driver = None

    def __verify_interface_data(self, page_block_list_info):
        """
        接收接收数据，并验证接口数据是否符合要求
        返回符合要求的列表，否则返回None
        :param navigation_name_list:
        :param driver:
        :return:
        """
        try:
            if not isinstance(page_block_list_info, list):  # 判断接口返回是否为列表
                logging.error('接口数据不是列表')
                self.driver.quit()

            if len(page_block_list_info) == 0:
                logging.error("接口数据为空")
                self.driver.quit()

            for block_list in page_block_list_info:
                if isinstance(block_list, list) and len(block_list) >= 1:  # 判断接口返回的区块是否为列表且长度是否大于等于1
                    for block_n in range(len(block_list)):
                        if block_n == 0:
                            if not isinstance(block_list[block_n], str):  # 判断区块名称是否为字符
                                logging.error('区块名称应为字符')
                                quit()
                        elif block_n == 1:
                            if not isinstance(block_list[block_n], int):  # 判断推荐位位置是否为整形
                                logging.error("推荐位信息应为整形")
                                quit()
                else:
                    quit()
            return page_block_list_info
        except Exception as e:
            logging.error(e)

    def __page_block_id(self, block_no):
        """
        获取推荐位id列表
        :param block_no: 区块号
        :return: 区块id列表
        """
        list_block_number = ''
        block_no_dict = {
            '001': 1, '002': 2, '003': 3, '004': 4, '005': 6, '006': 8, '007': 8, '008': 6, '009': 5, '010': 7,
            '011': 4, '012': 5, '013': 6, '014': 6, '015': 7, '016': 7, '017': 9, '018': 5, '019': 6, '020': 0,
            '021': 9, '022': 10, '023': 2, '024': 8, '025': 6, '026': 3, '027': 7, '028': 2, '029': 11,
            '030': 12, '031': 12, '032': 0,
        }
        if not isinstance(block_no, str):
            return None
        try:
            if block_no in block_no_dict.keys():
                list_block_number = (block_no_dict[block_no])

            return list_block_number
        except Exception as e:
            logging.error(e)

    def __verify(self, block_recommend_no, content_num):
        """
        点击确认键，进入详情页，判断视频是否正常起播
        :param driver:用例驱动
        # :param content_type:节目类型
        # :param  content_name :详情页标题
        :return:
        """
        try:
            list_page_attr = self.driver.current_activity  # 获取导航页页面属性
            logging.info('testCase:' + '获取导航页页面属性' + list_page_attr)
            time.sleep(2)

            print('点击确认键进入详情页')
            self.__move_direction(1, 23)  # 点击确认按钮，进入详情页
            logging.info('testCase:' + '点击确认按钮，进入详情页')
            time.sleep(8)
            detail_page_attr = self.driver.current_activity  # 获取详情页页面属性
            logging.info('testCase:' + '获取详情页页面属性' + detail_page_attr)

            if list_page_attr != detail_page_attr:
                detail_title_name = self.driver.find_element_by_id(self.detail_title_id).text
                logging.info('testCase:' + '获取详情页标题' + detail_title_name)

                # # 推荐位内容写回-----
                # fileProcess.interface_data_return(detail_title_name)

                # 进入详情页成功，判断视频是否正常播放(是否存在错误码和播放鉴权失败提示)
                elements = [self.err_code_xpath, self.err_auth_xpath]
                err_name_text = self.__elements_exist(self.driver, elements)
                print(err_name_text)
                logging.info('testCase:' + '错误码' + err_name_text)
                if err_name_text != '' and (u'失败' or u'错误' in err_name_text):

                    # 视频播放失败，点击返回按钮，退出详情页
                    logging.error('testCase' + '视频播放失败,节目详情页标题为#' + detail_title_name)

                    # 推荐位内容写回-----
                    Flag = False
                    # fileProcess.interface_data_return(block_recommend_no,content_num,detail_title_name,Flag)
                    self.__interface_data_return(Flag)
                    self.__move_direction(self.driver, 1, 4)  # 点击返回按钮，返回导航页

                else:
                    # 视频正常播放
                    logging.info('testCase:' + '视频正常播放，开始执行测试用例')
                    time.sleep(15)

                    # 推荐位内容写回-----
                    Flag = True
                    # fileProcess.interface_data_return(block_recommend_no,content_num,detail_title_name,Flag)
                    self.__interface_data_return(Flag)
                    self.__move_direction(self.driver, 1, 4)  # 点击返回按钮，返回导航页

            else:
                logging.error('testCase' + '无法进入详情页，第' + content_num + '个推荐位')
                # 推荐位内容写回-----
                Flag = False
                # fileProcess.interface_data_return(block_recommend_no,content_num,Flag)
                self.__interface_data_return(Flag)
        except Exception as e:
            print(e)

    def __find_element(self, id_or_xpath, n=20):
        """
        通过id或者xpath定位单个元素
        返回类型单个元素对象
        :param driver:
        :param id_or_xpath:
        :param n:
        :return:
        """
        for i in range(n):
            try:
                if id_or_xpath.startswith('/'):
                    ret = self.driver.find_element_by_xpath(id_or_xpath)
                else:
                    ret = self.driver.find_element_by_id(id_or_xpath)
                return ret
            except Exception as e:
                time.sleep(0.5)
                print(e)
                continue

    def __find_elements(self, id_or_xpath, n=40):
        """
        通过id或者xpath定位元素列表
        返回类型元素列表
        :param driver:
        :param id_or_xpath:
        :param n:
        :return:
        """
        for i in range(n):
            try:
                if id_or_xpath.startswith('/'):
                    ret = self.driver.find_elements_by_xpath(id_or_xpath)
                else:
                    ret = self.driver.find_elements_by_id(id_or_xpath)
                return ret
            except Exception as e:
                time.sleep(0.5)
                print(e)
                continue

    def __elements_exist(self, elements):
        """
        判断是否存在播放鉴权或者错误码
        :param driver:驱动
        :param elements:错误码和鉴权失败xpath
        :return: err_name 元素text属性
        """
        err_name = ''
        for element in elements:
            try:
                err_name = self.driver.find_element_by_xpath(element).text
                break
            except Exception as e:
                print(e)
                continue
        return err_name

    def __return_proper(self, element):
        """

        :param driver:驱动
        :param element:页面元素，判断点击返回键后，页面是否正常返回
        :return:
        """
        ele = ''
        try:
            if element.startswith('/'):
                ele = self.driver.find_elements_by_xpath(element)
            else:
                ele = self.driver.find_elements_by_id(element)
        except Exception as e:
            print(e)
        return ele

    def __move_direction(self, num, direction, duration=0.5):
        """
        焦点移动
        :param driver:
        :param num: 焦点移动次数
        :param direction: 焦点移动方向
        :param duration:
        :return:
        """
        dict_direction = {'19': 'Move up', '20': 'Move down',
                          '21': 'Move left', '22': 'Move right', '23': 'enter', '4': 'return'}
        if not isinstance(num, int) and not isinstance(direction, int) and not isinstance(duration, float):
            return None
        try:
            for i in range(num):
                self.driver.keyevent(direction)
                time.sleep(duration)
            if str(direction) in dict_direction.keys():
                logging.info(u"%s %s times" % (dict_direction[str(direction)], (i + 1)))
                print(u"%s %s次" % (dict_direction[str(direction)], (i + 1)))
        except Exception as e:
            logging.error(e)

    def __page_block_id(self, block_no):
        """
        获取推荐位id列表
        :param block_no: 区块号
        :return: 区块id列表
        """
        list_block_number = ''
        block_no_dict = {
            '001': 1, '002': 2, '003': 3, '004': 4, '005': 6, '006': 8, '007': 8, '008': 6, '009': 5, '010': 7,
            '011': 4, '012': 5, '013': 6, '014': 6, '015': 7, '016': 7, '017': 9, '018': 5, '019': 6, '020': 0,
            '021': 9, '022': 10, '023': 2, '024': 8, '025': 6, '026': 3, '027': 7, '028': 2, '029': 11,
            '030': 12, '031': 12, '032': 0,
        }
        if not isinstance(block_no, str):
            return None
        try:
            if block_no in block_no_dict.keys():
                list_block_number = (block_no_dict[block_no])

            return list_block_number
        except Exception as e:
            logging.error(e)

    def __get_navigation_class_xpath(self, navigation_info_dict):
        """
        根据配置文件信息获取需要的导航名称对应的xpath列表NavigationName_xpath_List
        存在二级导航：[{'cctv+':'First_Navigation_Xpath1'},{'cctv5':'First_Navigation_Xpath1'}]
        不存在二级导航：[{'ZWYTEST': '//android.support.v7.widget.RecyclerView[@index=2]/android.widget.FrameLayout[@index=2]/android.widget.TextView'}]
        无导航数据：[]
        :return: NavigationName_xpath_List  导航列表
        """
        navigation_name_xpath_list = []
        for key, value in navigation_info_dict.items():
            logging.info("key = " + str(key) + "value = " + str(value))
            nav_name_dict = {}  # 导航名称对应xpath的字典，格式：{'cctv+':['First_Navigation_Xpath1']}
            try:
                if key == 'first_class_navigation' and value != '':
                    first_navigation_xpath = self.first_class_xpath
                    value_first_navigation = value
                    logging.info("Value_First_Navigation:", value_first_navigation)
                    nav_name_dict[value_first_navigation] = first_navigation_xpath
                    navigation_name_xpath_list.append(nav_name_dict)

                elif key == 'second_class_navigation' and value != '':
                    second_navigation_xpath = self.second_class_xpath
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

    def __assert_target_navigation_len(self, navigation_info_dict):
        """
        验证导航对应xpath的列表是否为空，如果为空直接退出程序
        不为空，返回导航对应的xpath列表及列表长度
        :return: (NavigationName_xpath_List,LenNavigationName_xpath_List)元组
        """
        navigation_name_xpath_list = self.__get_navigation_class_xpath(navigation_info_dict)
        len_navigation_name_xpath_list = len(navigation_name_xpath_list)
        try:
            if len_navigation_name_xpath_list == 0:
                logging.error("导航信息为空")
                quit()
            else:
                return navigation_name_xpath_list, len_navigation_name_xpath_list
        except Exception as e:
            print(e)

    def __find_target_navigation(self, navigation_info_dict):
        """
        导航信息不为空时，移动导航焦点找到目标导航
        :param driver:
        :return: 目标导航列表
        """
        navigation_name_xpath_list, len_navigation_name_xpath_list = self.__assert_target_navigation_len(navigation_info_dict)
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
                    while n <= self.navigation_count:
                        logging.info("导航焦点右移循环次数共20次，当前次数为：%s次" % n)
                        try:
                            navigation_name = self.__find_element(value)
                            logging.info(navigation_name.text)
                            logging.info("导航名称:", navigation_name.text)
                            if navigation_name.text == key:
                                navigation_name_list.append(navigation_name.text)
                                if i == 0:
                                    class_name = chr(i + 19968)
                                else:
                                    class_name = chr(i + 20107)
                                logging.info("找到了%s级导航%s" % (class_name, navigation_name.text))
                                print("找到了%s级导航%s" % (class_name, navigation_name.text))
                                break
                            else:
                                # 未找到要找的导航名称时右移一次焦点
                                self.__move_direction(1, 22)
                            n += 1
                        except Exception as e:
                            logging.info('未定位到导航，右移焦点')
                            self.__move_direction(1, 22)
                            n += 1
                            print(e)
                    time.sleep(self.navigation_wait_time)
                    # 找到要测试的导航时，下移一次焦点
                    self.__move_direction(1, 20)
        # 返回要测试的导航名称列表
        return navigation_name_list

    def __get_navigation_name(self, navigation_info_dict):
        """
        判断目标导航列表是否为空，如果为空退出程序
        目标导航不为空，返回目标导航列表
        :param driver:
        :return: 导航列表
        """
        navigation_name_list = self.__find_target_navigation(navigation_info_dict)
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

    def __interface_block_no_content_travel(self, block_no_content_list, block_recommend_no):
        """
        遍历接口与当前遍历推荐位对比
        :param driver:
        :param block_no_content_list: 推荐位信息列表
        :param block_recommend_no: 推荐位编号
        :return:
        """
        # 遍历接口信息：需要测试的推荐位内容
        # for content_dict_no in range(len(block_no_content_list)):
        #     print(content_dict_no)  #推荐位字典
        #     print(block_no_content_list[content_dict_no])  # 每一个推荐位内容为字典格式
        #     if block_recommend_no in block_no_content_list[content_dict_no].keys():
        #         content_num = str(content_dict_no+1)  # 匹配上的推荐位的第几个
        #         print(content_num)
        #         content_type = block_no_content_list[content_dict_no][block_recommend_no][0]  # 推荐位的详情页类型
        #         content_name = block_no_content_list[content_dict_no][block_recommend_no][1]  # 推荐位的详情页名称
        #         print('---------------点击推荐位进入详情页并返回-----------', content_type, content_name, content_num)
        #
        #         # 调用用例方法，运行对应用例
        #         paramAndPlay.verify(driver, content_type, content_name)

        # block_no_content_list = [0]
        for content_no in block_no_content_list:
            print(content_no)
            if content_no == block_recommend_no:
                content_num = str(content_no + 1)
                print(content_num)
                # print('---------------点击推荐位进入详情页并返回-----------', content_type, content_name, content_num)
                print('---------------点击推荐位进入详情页并返回-----------', content_num)
                # 调用用例方法，运行对应用例
                # paramAndPlay.verify(driver, content_type, content_name)
                self.__verify(block_recommend_no, content_num)

                # 判断当前页面是否为频道页
                while True:
                    try:
                        if self.__find_element(self.first_class_xpath):
                            print('在频道页移动焦点到下一个推荐位')
                            break
                    except Exception as e:
                        print(e)
                        self.__move_direction(1, 4)
                break

    def __block_001_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，1号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if not isinstance(i, int):
            return None
        if i == 0:
            logging.info('焦点不移动')

    def __block_002_023_028_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，2\23\28号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 1:
            logging.info('区块最后一个推荐位')

    def __block_003_026_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，3\26号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i in [0, 1]:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            logging.info('区块最后一个推荐位')

    def __block_004_011_play_focus_move(self, i):
        """
         处理区遍历块推荐位时焦点的移动，4\11号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 3:
            logging.info('区块最后一个推荐位')

    def __block_008_005_025_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，8\5\25号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 3:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 4:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 5:
            logging.info('区块最后一个推荐位')

    def __block_006_007_024_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，6\7\24号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 3:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 4:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 5:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 6:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 7:
            logging.info('区块最后一个推荐位')

    def __block_009_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，9号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 1:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 2:
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 3:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 4:
            logging.info('区块最后一个推荐位')

    def __block_010_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，10号区块
        :param driver:
        :param i:区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 1:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 2:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 3:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 4:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 5:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 6:
            logging.info('区块最后一个推荐位')

    def __block_012_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，12号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 3:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 4:
            logging.info('区块最后一个推荐位')

    def __block_013_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，13号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 3:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 4:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 5:
            logging.info('区块最后一个推荐位')

    def __block_014_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，14号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        ***恢复焦点时多下移一次***
        :return:
        """
        if i == 0:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 1:
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 2:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 3:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 4:
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 5:
            logging.info('区块最后一个推荐位')

    def __block_015_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，15号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 3:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 4:
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 5:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 6:
            logging.info('区块最后一个推荐位')

    def __block_016_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，16号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 3:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 4:
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 5:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 6:
            logging.info('区块最后一个推荐位')

    def __block_017_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，17号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 左移1次
            self.__move_direction(1, 21)
            logging.info('焦点左移1次')
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 3:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 4:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
            # 左移3次
            self.__move_direction(3, 21)
            logging.info('焦点左移3次')
        elif i == 5:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 6:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 7:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 8:
            logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')

    def __block_018_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，18号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        ***恢复焦点时多下移一次**
        :return:
        """
        if i == 0:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 1:
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 3:
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 4:
            logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')

    def __block_019_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，19号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 3:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
            # 左移1次
            self.__move_direction(1, 21)
            logging.info('焦点左移1次')
        elif i == 4:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 5:
            logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')

    def __block_021_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，21号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 左移2次
            self.__move_direction(2, 21)
            logging.info('焦点左移2次')
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 3:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 4:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 5:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 6:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 7:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 8:
            logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')

    def __block_022_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，22号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 3:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移2次
            self.__move_direction(2, 19)
            logging.info('焦点上移2次')
        elif i == 4:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 5:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 6:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移2次
            self.__move_direction(2, 19)
            logging.info('焦点上移2次')
        elif i == 7:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 8:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 9:
            logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')

    def __block_027_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，27号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 左移2次
            self.__move_direction(2, 21)
            logging.info('焦点左移2次')
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 3:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 4:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 5:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 6:
            logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')

    def __block_029_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，29号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
            # 左移1次
            self.__move_direction(1, 21)
            logging.info('焦点左移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 2:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移2次
            self.__move_direction(2, 19)
            logging.info('焦点上移2次')
        elif i == 3:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 4:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
            # 左移1次
            self.__move_direction(1, 21)
            logging.info('焦点左移1次')
        elif i == 5:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 6:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移2次
            self.__move_direction(2, 19)
            logging.info('焦点上移2次')
        elif i == 7:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 8:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
            # 左移1次
            self.__move_direction(1, 21)
            logging.info('焦点左移1次')
        elif i == 9:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 10:
            logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')

    def __block_030_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，30号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 1:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 2:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 3:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 4:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 5:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 6:

            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 7:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 8:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 9:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 10:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 11:
            logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')

    def __block_031_play_focus_move(self, i):
        """
        处理区遍历块推荐位时焦点的移动，31号区块
        :param driver:
        :param i: 区块推荐位列表序列号，即区块的第几个推荐位
        :return:
        """
        if i == 0:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 1:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 2:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 3:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 4:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
            # 上移1次
            self.__move_direction(1, 19)
            logging.info('焦点上移1次')
        elif i == 5:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
        elif i == 6:
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('焦点下移1次')
            # 左移1次
            self.__move_direction(3, 21)
            logging.info('焦点左移3次')
        elif i == 7:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 8:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 9:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 10:
            # 右移1次
            self.__move_direction(1, 22)
            logging.info('焦点右移1次')
        elif i == 11:
            logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')

    def __page_block_focus_move(self, block_no_name, block_recommend_no):
        """
        根据区块号确定调用区块的焦点移动函数
        :param driver:
        :param block_num: 区块号
        :param recommended_num: 推荐位号
        :return:
        """
        try:
            if block_no_name == "001":
                self.__block_001_play_focus_move(block_recommend_no)
            elif block_no_name in "002_023_028":
                self.__block_002_023_028_play_focus_move(block_recommend_no)
            elif block_no_name in "003_026":
                self.__block_003_026_play_focus_move(block_recommend_no)
            elif block_no_name in "004_011":
                self.__block_004_011_play_focus_move(block_recommend_no)
            elif block_no_name in "008_005_025":
                self.__block_008_005_025_play_focus_move(block_recommend_no)
            elif block_no_name in "006_007_024":
                self.__block_006_007_024_play_focus_move(block_recommend_no)
            elif block_no_name == "009":
                self.__block_009_play_focus_move(block_recommend_no)
            elif block_no_name == "010":
                self.__block_010_play_focus_move(block_recommend_no)
            elif block_no_name == "012":
                self.__block_012_play_focus_move(block_recommend_no)
            elif block_no_name == "013":
                self.__block_013_play_focus_move(block_recommend_no)
            elif block_no_name == "014":
                self.__block_014_play_focus_move(block_recommend_no)
            elif block_no_name == "015":
                self.__block_015_play_focus_move(block_recommend_no)
            elif block_no_name == "016":
                self.__block_016_play_focus_move(block_recommend_no)
            elif block_no_name == "017":
                self.__block_017_play_focus_move(block_recommend_no)
            elif block_no_name == "018":
                self.__block_018_play_focus_move(block_recommend_no)
            elif block_no_name == "019":
                self.__block_019_play_focus_move(block_recommend_no)
            elif block_no_name == "021":
                self.__block_021_play_focus_move(block_recommend_no)
            elif block_no_name == "022":
                self.__block_022_play_focus_move(block_recommend_no)
            elif block_no_name == "027":
                self.__block_027_play_focus_move(block_recommend_no)
            elif block_no_name == "029":
                self.__block_029_play_focus_move(block_recommend_no)
            elif block_no_name == "030":
                self.__block_030_play_focus_move(block_recommend_no)
            elif block_no_name == "031":
                self.__block_031_play_focus_move(block_recommend_no)
            else:
                logging.error("can't find " + block_no_name + " move method")
        except Exception as e:
            logging.error(e)

    def __page_block_focus_move_return(self, block_name):
        """
        '''
        根据区块号确定区块内推荐位焦点的返回，将焦点移动到区块的最左侧
        :param driver:
        :param block_name: 区块号
        :return:
        """
        if block_name == '001':
            pass

        elif block_name in ['002', '023', '028']:
            # 左移1次
            self.__move_direction(1, 21)
            logging.info('左移1次')

        elif block_name in ['003', '009', '012', '026']:
            # 左移2次
            self.__move_direction(2, 21)
            logging.info('左移2次')

        elif block_name in ['004', '010', '011', '013', '015', '016', '017', '019', '027', '031']:
            # 左移3次
            self.__move_direction(3, 21)
            logging.info('左移3次')

        elif block_name in ['005', '008', '021', '025', '029', '030']:
            # 左移5次
            self.__move_direction(5, 21)
            logging.info('左移5次')

        elif block_name in ['006', '007', '024']:
            # 左移7次
            self.__move_direction(7, 21)
            logging.info('左移7次')

        elif block_name == '014':
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('下移1次')
            # 左移2次
            self.__move_direction(2, 21)
            logging.info('左移2次')

        elif block_name == '018':
            # 下移1次
            self.__move_direction(1, 20)
            logging.info('下移1次')
            # 左移1次
            self.__move_direction(1, 21)
            logging.info('左移1次')

        elif block_name == '020':
            logging.info('not 20')

        elif block_name == '022':
            # 左移4次
            self.__move_direction(4, 21)
            logging.info('左移4次')

        elif block_name == '032':
            logging.info('not found num 32')

    def __block_recommend_travel_have_target(self, list_block_number, block_no_name, block_no_content_list):
        """
        有测试推荐位的区块遍历
        :param driver:
        :param list_block_number  区块的推荐位数量
        :param block_no_name      区块名称
        :param block_no_content_list    推荐位信息列表
        :return:
        """
        # 遍历当前区块推荐位
        for block_recommend_no in range(list_block_number):
            block_recommend_num = block_recommend_no + 1  # 遍历数从0开始，为了显示数量从1开始计数
            logging.info('当前区块%s的第%s个位置' % (block_no_name, block_recommend_num))

            if block_no_content_list == []:
                logging.info('无推荐位遍历')
            elif block_no_content_list != []:
                # 需要测试的推荐位内容
                self.__interface_block_no_content_travel(block_no_content_list, block_recommend_no)

            # print (block_no_name, block_recommend_no)
            # print(type(block_no_name),type(block_recommend_no))
            # 根据区块名称，推荐位编号移动焦点
            self.__page_block_focus_move(block_no_name, block_recommend_no)

        # 2.6、区块推荐位遍历完成恢复区块焦点位置
        self.__page_block_focus_move_return(block_no_name)
        # 向下移动焦点
        self.__move_direction(1, 20)

    def __page_block_traversal(self, navigation_name_list, page_block_list_info):
        """
        频道页区块遍历
        :param driver:
        :param navigation_name_list: 接口信息列表
        :return:
        """
        # 验证页面接口数据的正确性
        page_block_list = self.__verify_interface_data(page_block_list_info)
        print(page_block_list)
        # page_block_list = [['004', 0]]
        # 判断是否有二级导航（1、增加二级导航判断，确定当前频道页名称）
        if navigation_name_list[-1] == '':
            channel_name = navigation_name_list[0]
        else:
            channel_name = navigation_name_list[-1]
        # channel_name 导航页名称

        try:
            # 页面区块长度
            len_page_block_list = len(page_block_list)
            logging.info(channel_name + '频道共有区块%s个' % len_page_block_list)

            # 2、遍历页面区块的数量
            for block_num_serial in range(len_page_block_list):
                block_num = block_num_serial + 1  # 页面区块编号
                len_block_list = len(page_block_list[block_num_serial])  # 区块长度

                if len_block_list >= 1:
                    block_no_name = page_block_list[block_num_serial][0]  # 获取区块名称
                    logging.info('------%s频道页第%s个区块：%s------' % (channel_name, block_num, block_no_name))

                    # 3、生成当前区块的推荐位数量
                    list_block_number = self.__page_block_id(block_no_name)
                    print(list_block_number)

                    block_no_content_list = page_block_list[block_num_serial][1:]  # 推荐位信息列表
                    logging.info(block_no_content_list)
                    self.__block_recommend_travel_have_target(list_block_number, block_no_name, block_no_content_list)
            print("=====退出=====")
        except Exception as e:
            logging.error(e)

    def __interface_data_processing(self, interface_data):
        '''
        读取配置文件，将文件内容分离目标导航数据、目标导航页面数据两部分；
        并将分离后的数据处理成目标导航字典，目标导航页面数据列表
        :param file_path 接口数据文件名称
        :return navigation_info_dict,page_block_list_info  目标导航字典，目标导航页面数据列表
        '''
        # 导航字典
        navigation_info_dict = {'first_class_navigation': '', 'second_class_navigation': ''}
        navigation_data = interface_data[:2]
        navigation_info_dict['first_class_navigation'] = navigation_data[0]
        navigation_info_dict['second_class_navigation'] = navigation_data[-1]
        # 页面接口数据
        page_block_list_info = interface_data[-1]
        # print (navigation_info_dict,page_block_list_info)
        return navigation_info_dict, page_block_list_info

    # 先写一个假函数把流程串起来，主要把参数传进来
    def click(self, infoDict):
        navigation_info_dict,page_block_list_info = self.__interface_data_processing(infoDict)
        navigation_name_list = self.__get_navigation_name(navigation_info_dict)
        logging.info(navigation_name_list)

        self.__page_block_traversal(navigation_name_list, page_block_list_info)

    def connect(self):
        try:
            desired_caps = {
                'deviceName': "14499M580068257",  # 设备信息，adb devices命令得到的值
                'platformName': "Android",  # 系统信息，Android/IOS
                'platformVersion': "5.1",  # 系统版本号
                'automationName': "Appium",  # Appium
                'appPackage': "com.newtv.cboxtv",  # 被测试apk包名
                'appActivity': "tv.newtv.cboxtv.EntryActivity",  # 被测试apk启动页
                'appWaitActivity': "tv.newtv.cboxtv.MainActivity",  # 填写测试包等待页
                'noReset': True,  # 不要在会话前重置应用状态
                'unicodeKeyboard': True,  # 使用 Unicode 输入法
                'resetKeyboard': True,  # Unicode 测试结束后，重置输入法到原有状态
                'newCommandTimeout': 24000,  # 设置过期时间

            }
            self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
            # self.driver.find_elements_by_xpath(self.logo_xpath)

            return True
        except Exception as e:
            logging.error("appium链接错误")
            return False

    def disconnect(self):
        self.driver.quit()

    def channel(self, channelId):
        pass

    def program(self, contentId):
        pass
