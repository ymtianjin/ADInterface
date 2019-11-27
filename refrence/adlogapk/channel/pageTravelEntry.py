# encoding=utf-8
__author__ = 'lqq'
# 遍历区块
import logging
from channel import blockRecomendTravel
from util import pageBlockID
from interface import interfaceVerify


def page_block_traversal(driver,navigation_name_list,page_block_list_info):
    """
    频道页区块遍历
    :param driver:
    :param navigation_name_list: 接口信息列表
    :return:
    """
    # 验证页面接口数据的正确性
    page_block_list = interfaceVerify.verify_interface_data(page_block_list_info, driver)
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
        logging.info(channel_name+'频道共有区块%s个' % len_page_block_list)

        # 2、遍历页面区块的数量
        for block_num_serial in range(len_page_block_list):
            block_num = block_num_serial+1  # 页面区块编号
            len_block_list = len(page_block_list[block_num_serial])#区块长度

            if len_block_list >= 1:
                block_no_name = page_block_list[block_num_serial][0]                # 获取区块名称
                logging.info('------%s频道页第%s个区块：%s------' % (channel_name, block_num, block_no_name))

                # 3、生成当前区块的推荐位数量
                list_block_number = pageBlockID.page_block_id(block_no_name)
                print(list_block_number)

                block_no_content_list = page_block_list[block_num_serial][1:]  #推荐位信息列表
                logging.info(block_no_content_list)
                blockRecomendTravel.block_recommend_travel_have_target(driver, list_block_number,block_no_name, block_no_content_list)
        print("=====退出=====")
    except Exception as e:
        logging.error(e)
