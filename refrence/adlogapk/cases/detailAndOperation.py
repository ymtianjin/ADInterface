# encoding=utf-8
import logging

from log import programLog

__author__ = 'zhangwy'
import time
from util import fileProcess, readConfig, focusMove, locateElement
from util.const import Const
from util.fileProcess import time_convert


class DetailAndOperation(object):
    """
    用例设计类
    """

    movie_length1 = ''  # 第一个节目的节目时长
    movie_length2 = ''  # 第二个节目的节目时长
    movie_length3 = ''  # 第三个节目的节目时长

    def __init__(self):

        self.nodes = readConfig.read_config("Log-Node")
        self.flag1 = ':0'  # 第一个节目标签
        self.flag2 = ':1'  # 第二个节目标签
        self.flag3 = ':2'  # 第三个节目标签
        self.flag_seek = ':seek'  # 持续执行seek操作，直到节目自动播放完毕标签

    def play(self, driver, content_type, content_num):
        """
        点击确认按钮，大屏起播
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:

            video_flag = '#'+content_num+self.flag1

            # TV上报（1|1）日志，其他类型上报（13|0）日志
            if content_type == 'TV':
                fileProcess.write_txt_file(self.nodes.get('playRec') + video_flag + '\n'
                                           + self.nodes.get('playColumn') + video_flag, Const.except_file_path)
                logging.info('testCase:' + '节目类型为TV的预期结果' + content_type)
            else:
                fileProcess.write_txt_file(self.nodes.get('playRec') + video_flag + '\n'
                                           + self.nodes.get('playDetail') + video_flag, Const.except_file_path)
                logging.info('testCase:' + '其他类型节目的预期结果' + content_type)
            fileProcess.write_txt_file(self.nodes.get('playHis') + video_flag + '\n'
                                       + self.nodes.get('playStart') + video_flag + '\n'
                                       + self.nodes.get('playRe') + video_flag + '\n'
                                       + self.nodes.get('playActual') + video_flag, Const.except_file_path)
            try:
                print("判断是否存在购买按钮")
                driver.find_element_by_id(Const.vip_id)
                fileProcess.write_txt_file('chargeType:'+'1,1,1', Const.result_file_path)
                logging.info('testCase:' + '详情页存在购买按钮，该节目集付费')
            except Exception as e:
                fileProcess.write_txt_file('chargeType:' + '0,0,0', Const.result_file_path)
                print(e)
                logging.info('testCase:' + '详情页不存在购买按钮，该节目集免费')

            focusMove.move_direction(driver, 1, 23)  # 点击确认按钮，全屏播放
            logging.info('testCase:' + '点击确认按钮，进入全屏播放')
            fileProcess.write_txt_file(self.nodes.get('playWindow') + video_flag, Const.except_file_path)
        except Exception as e:
            print(e)
            programLog.error_log(e)

    def pause(self, driver, content_type, content_num):
        """
        点击确认按钮，暂停开始和结束
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:
            video_flag = '#' + content_num + self.flag1
            time.sleep(20)  # 休息时间设为20s

            focusMove.move_direction(driver, 1, 23)  # 点击确认键，暂停开始
            print("===暂停开始===")

            fileProcess.write_txt_file(self.nodes.get('pauseStart') + video_flag, Const.except_file_path)

            pause_time = locateElement.find_element(driver, Const.left_time).text
            print("暂停位置:" + pause_time)
            logging.info('testCase:' + '点击确认按钮，暂停开始，暂停位置为' + pause_time)

            global movie_length1
            movie_length1 = locateElement.find_element(driver, Const.right_time).text
            print("第一个视频节目时长:" + movie_length1)
            logging.info('testCase:' + '第一个视频节目时长为：' + movie_length1)

            # 将暂停位置信息写入预期结果
            fileProcess.write_txt_file('pause_location:' + time_convert(pause_time), Const.result_file_path)

            time.sleep(5)
            focusMove.move_direction(driver, 1, 23)  # 点击确认键，暂停结束
            print("===暂停结束===")
            fileProcess.write_txt_file(self.nodes.get('pauseOver') + video_flag, Const.except_file_path)
            logging.info('testCase:' + '点击确认按钮，暂停结束')
        except Exception as e:
            print(e)
            programLog.error_log(e)

    def select(self, driver, content_type, content_num):
        """
        呼出和隐藏选集页
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:
            video_flag = '#' + content_num + self.flag1
            print("===点击菜单键，调出选集页===")
            time.sleep(10)  # 设置等待时间为10s

            focusMove.move_direction(driver, 1, 23)  # 点击确认键，暂停开始
            fileProcess.write_txt_file(self.nodes.get('pauseStart') + video_flag, Const.except_file_path)
            # time.sleep(2)

            # 获取当前时间，作为呼出选集页location值
            select_time = locateElement.find_element(driver, Const.left_time).text
            print("调出选集页位置:" + select_time)
            logging.info('testCase:' + '点击确认按钮，暂停开始，呼出选集页位置为：' + select_time)

            # 将呼出选集页位置信息写入预期结果文件
            fileProcess.write_txt_file('select_time:' + time_convert(select_time), Const.result_file_path)

            focusMove.move_direction(driver, 1, 20)  # 点击向下按钮，调出选集页

            # 上报调出选集页节点日志
            fileProcess.write_txt_file(self.nodes.get('selectStart') + video_flag, Const.except_file_path)

            # 5s后，自动隐藏选集页，上报隐藏选集页节点日志
            time.sleep(6)  # 5s自动隐藏选集页
            fileProcess.write_txt_file(self.nodes.get('selectOver') + video_flag, Const.except_file_path)

            focusMove.move_direction(driver, 1, 23)  # 点击确认键，节目开始播放
            fileProcess.write_txt_file(self.nodes.get('pauseOver') + video_flag, Const.except_file_path)
        except Exception as e:
            print(e)
            programLog.error_log(e)

    def seek(self, driver, content_type, content_num):
        """
        点击快进按钮，执行seek操作
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:
            video_flag = '#' + content_num + self.flag1
            print("===点击快进按钮，执行seek操作===")
            time.sleep(10)  # 设置等待时间为10s
            focusMove.move_direction(driver, 1, 23)  # 点击确认键，暂停开始
            fileProcess.write_txt_file(self.nodes.get('pauseStart') + video_flag, Const.except_file_path)
            # time.sleep(2)

            # 获取当前时间，作为seek开始location值
            seek_start = locateElement.find_element(driver, Const.left_time).text
            print("seek开始位置:" + seek_start)
            logging.info('testCase:' + '点击确认按钮，暂停开始，seek开始位置为：' + seek_start)

            # 将seek开始位置信息写入预期结果文件
            fileProcess.write_txt_file('seek_start:' + time_convert(seek_start), Const.result_file_path)

            focusMove.move_direction(driver, 1, 22)  # 点击向右按钮，执行一次seek操作
            time.sleep(2)
            logging.info('testCase:' + '点击向右按钮，执行seek操作##快进##')

            # 上报seek开始和结束节点日志
            fileProcess.write_txt_file(self.nodes.get('seekStart') + video_flag + '\n'
                                       + self.nodes.get('seekOver') + video_flag, Const.except_file_path)

            # 获取seek结束后位置信息，写入预期结果文件
            seek_over = driver.find_element_by_id(Const.left_time).text
            print("seek结束位置:" + seek_over)
            fileProcess.write_txt_file('seek_over:' + time_convert(seek_over), Const.result_file_path)
            logging.info('testCase:' + 'seek结束位置为：' + seek_over)
            time.sleep(10)
        except Exception as e:
            print(e)
            programLog.error_log(e)

    def back(self, driver, content_type, content_num):
        """
        点击快退按钮，执行seek操作
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:
            video_flag = '#' + content_num + self.flag1
            print("===点击向左按钮，执行快退操作===")
            focusMove.move_direction(driver, 1, 23)  # 点击确认键，暂停开始
            fileProcess.write_txt_file(self.nodes.get('pauseStart') + video_flag, Const.except_file_path)
            # time.sleep(2)

            # 获取当前时间，作为快退开始的location值
            back_start = locateElement.find_element(driver, Const.left_time).text
            print("快退开始位置:" + back_start)
            logging.info('testCase:' + '点击确认按钮，暂停开始，快退开始位置为：' + back_start)

            # 将快退开始位置信息写入预期结果文件
            fileProcess.write_txt_file('back_start:' + time_convert(back_start), Const.result_file_path)

            focusMove.move_direction(driver, 1, 21)  # 点击向左按钮，执行一次快退操作
            time.sleep(2)
            logging.info('testCase:' + '点击向左按钮，执行seek操作##快退##')

            # 上报seek开始和结束节点日志
            fileProcess.write_txt_file(self.nodes.get('seekStart') + video_flag + '\n'
                                       + self.nodes.get('seekOver') + video_flag, Const.except_file_path)

            # 获取快退结束后位置信息，写入预期结果文件
            back_over = driver.find_element_by_id(Const.left_time).text
            print("快退结束位置:" + back_over)
            fileProcess.write_txt_file('back_over:' + time_convert(back_over), Const.result_file_path)
            logging.info('testCase:' + 'back结束位置为：' + back_over)
            time.sleep(10)
        except Exception as e:
            print(e)
            programLog.error_log(e)

    def drop(self, driver, content_type, content_num):

        """
        手动退出播放
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:
            video_flag = '#' + content_num + self.flag1
            print("===点击返回按钮，手动退出播放===")
            focusMove.move_direction(driver, 1, 23)  # 点击确认键，暂停开始
            fileProcess.write_txt_file(self.nodes.get('pauseStart') + video_flag, Const.except_file_path)
            # time.sleep(2)

            # 获取当前时间，作为手动退出时location值
            drop_time = locateElement.find_element(driver, Const.left_time).text
            print("手动退出播放位置:" + drop_time)
            logging.info('testCase:' + '点击确认按钮，暂停开始，手动退出位置为：' + drop_time)

            # 将手动退出播放位置信息写入预期结果文件
            fileProcess.write_txt_file('drop_time:' + time_convert(drop_time), Const.result_file_path)
            time.sleep(5)

            focusMove.move_direction(driver, 2, 4, 1)  # 连续点击两次返回按钮，返回导航页
            time.sleep(2)
            # 判断是否正常返回导航页
            element = locateElement.return_proper(driver, Const.first_class_xpath)
            while element == '':
                focusMove.move_direction(driver, 1, 4)
                time.sleep(2)
                element = locateElement.return_proper(driver, Const.first_class_xpath)

            fileProcess.write_txt_file(self.nodes.get('playWindow') + video_flag + '\n'
                                       + self.nodes.get('pauseOver') + video_flag + '\n'
                                       + self.nodes.get('playDrop') + video_flag, Const.except_file_path)
        except Exception as e:
            print(e)
            programLog.error_log(e)

    def reenter(self, driver, content_type, content_num):
        """
        验证断点续播日志
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:
            video_flag = '#' + content_num + self.flag1
            print("===断点续播===")
            time.sleep(5)  # 设置等待时间为5s

            focusMove.move_direction(driver, 2, 23, 3)  # 连续点击两次确认按钮，全屏播放
            logging.info('testCase' + '连续点击两次确认按钮，视频全屏播放')
            # TV上报（1|1）日志，其他类型上报（13|0）日志
            if content_type == 'TV':
                fileProcess.write_txt_file(self.nodes.get('playRec') + video_flag + '\n'
                                           + self.nodes.get('playColumn') + video_flag, Const.except_file_path)
            else:
                fileProcess.write_txt_file(self.nodes.get('playRec') + video_flag + '\n'
                                           + self.nodes.get('playDetail') + video_flag, Const.except_file_path)
            fileProcess.write_txt_file(self.nodes.get('playHis') + video_flag + '\n'
                                       + self.nodes.get('playStart') + video_flag + '\n'
                                       + self.nodes.get('seekStart') + video_flag + '\n'
                                       + self.nodes.get('seekOver') + video_flag + '\n'
                                       + self.nodes.get('playRe') + video_flag + '\n'
                                       + self.nodes.get('playActual') + video_flag + '\n'
                                       + self.nodes.get('playWindow') + video_flag, Const.except_file_path)
        except Exception as e:
            print(e)
            programLog.error_log(e)

    def expired(self, driver, content_type, content_num):
        """
        执行seek操作，直到视频播放结束
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:
            video_seek_flag = '#' + content_num + self.flag_seek
            video_flag = '#' + content_num + self.flag1
            print("===执行seek操作，直到自动播放结束===")
            time.sleep(10)  # 设置等待时间为10s

            global movie_length1
            movie_length1_convert = time_convert(movie_length1)
            seek_num = int(movie_length1_convert)//32000

            logging.info('testCase' + '需要持续执行seek次数:' + str(seek_num))
            focusMove.move_direction(driver, seek_num, 22)
            time.sleep(1)
            current_time = driver.find_element_by_id(Const.left_time).text
            current_time_convert = time_convert(current_time)
            logging.info('testCase' + '持续执行seek操作之后的位置为:' + current_time_convert)
            for i in range(1, seek_num):
                fileProcess.write_txt_file(self.nodes.get('seekStart') + video_seek_flag + '\n'
                                           + self.nodes.get('seekOver') + video_seek_flag, Const.except_file_path)

            while int(movie_length1_convert) - int(current_time_convert) > 30000:
                focusMove.move_direction(driver, 1, 22)  # 点击向右按钮，执行seek操作
                time.sleep(1)
                current_time = driver.find_element_by_id(Const.left_time).text
                current_time_convert = time_convert(current_time)
                logging.info('testCase' + '执行seek操作，当前位置为：' + current_time_convert)
                fileProcess.write_txt_file(self.nodes.get('seekStart') + video_seek_flag + '\n'
                                           + self.nodes.get('seekOver') + video_seek_flag, Const.except_file_path)

            fileProcess.write_txt_file(self.nodes.get('playDrop') + video_flag, Const.except_file_path)
        except Exception as e:
            print(e)
            programLog.error_log(e)

    def proceed(self, driver, content_type, content_num):
        """
        自动续播下一集
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:
            video_flag = '#' + content_num + self.flag2
            print("===自动续播下一集===")
            time.sleep(90)  # 设置等待时间为90s
            focusMove.move_direction(driver, 1, 23)  # 点击确认按钮，暂停开始
            # time.sleep(2)

            global movie_length2
            movie_length2 = locateElement.find_element(driver, Const.right_time).text
            print("第二个视频节目时长:" + movie_length2)
            logging.info('testCase' + '点击确认按钮，获取第二个视频时长，时长为：' + movie_length2)

            time.sleep(10)  # 设置等待时间为10s
            focusMove.move_direction(driver, 1, 4)  # 点击返回按钮，返回详情页
            time.sleep(2)
            element = locateElement.return_proper(driver, Const.detail_title_id)
            while element == '':
                focusMove.move_direction(driver, 1, 4)
                time.sleep(2)
                element = locateElement.return_proper(driver, Const.detail_title_id)
            time.sleep(3)

            fileProcess.write_txt_file(self.nodes.get('playStart') + video_flag + '\n'
                                       + self.nodes.get('playRe') + video_flag + '\n'
                                       + self.nodes.get('playActual') + video_flag + '\n'
                                       + self.nodes.get('pauseStart') + video_flag + '\n'
                                       + self.nodes.get('playWindow') + video_flag + '\n'
                                       + self.nodes.get('pauseOver') + video_flag, Const.except_file_path)
        except Exception as e:
            print(e)
            programLog.error_log(e)

    def detail(self, driver, content_type, content_num):
        """
        详情页选集操作
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:
            video_flag2 = '#' + content_num + self.flag2
            video_flag3 = '#' + content_num + self.flag3
            print("===详情页选集操作===")
            time.sleep(2)

            focusMove.move_direction(driver, 1, 20)  # 点击向下按钮
            time.sleep(2)

            focusMove.move_direction(driver, 1, 22)  # 点击向右按钮
            time.sleep(2)

            focusMove.move_direction(driver, 1, 23)  # 点击确认按钮
            time.sleep(20)

            fileProcess.write_txt_file(self.nodes.get('playDrop') + video_flag2 + '\n'
                                       + self.nodes.get('playWindow') + video_flag2 + '\n'
                                       + self.nodes.get('playStart') + video_flag3 + '\n'
                                       + self.nodes.get('playRe') + video_flag3 + '\n'
                                       + self.nodes.get('playActual') + video_flag3, Const.except_file_path)

            focusMove.move_direction(driver, 1, 23)  # 点击确认按钮，暂停开始
            # time.sleep(2)

            global movie_length3
            movie_length3 = locateElement.find_element(driver, Const.right_time).text
            print("第三个视频节目时长:" + movie_length3)
            # print(movie_length3)
            print(type(movie_length3))
            logging.info('testCase' + '点击暂停按钮，获取第三个视频时长，时长为:' + movie_length3)
            fileProcess.write_txt_file(self.nodes.get('pauseStart') + video_flag3
                                       , Const.except_file_path)

        except Exception as e:
            print(e)
            programLog.error_log(e)

    def over(self, driver, content_type, content_num):
        """
        退出播放
        :param driver:用例驱动
        :param content_type:节目类型
        :param content_num:计数器，第几个推荐位
        :return:
        """
        try:
            video_flag3 = '#' + content_num + self.flag3

            time.sleep(5)   # 设置等待时间为5s

            movie_length = [time_convert(movie_length1), ',', time_convert(movie_length2), ',',
                            time_convert(movie_length3)]
            fileProcess.write_txt_file('movieLength:' + ''.join(movie_length), Const.result_file_path)

            focusMove.move_direction(driver, 2, 4, 2)
            fileProcess.write_txt_file(self.nodes.get('playWindow') + video_flag3 + '\n'
                                       + self.nodes.get('pauseOver') + video_flag3 + '\n'
                                       + self.nodes.get('playDrop') + video_flag3, Const.except_file_path)
        except Exception as e:
            print(e)
            programLog.error_log(e)
