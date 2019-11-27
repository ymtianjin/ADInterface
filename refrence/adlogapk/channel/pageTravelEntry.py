# encoding=utf-8
import logging

from channel import blockRecomendTravel
from util import pageBlockID
from interface import interfaceVerify


def page_block_traversal(driver, navigation_name_list):
    """
    频道页遍历
    :param driver:
    :param navigation_name_list: 接口信息列表
    :return:
    """
    page_block_list = interfaceVerify.verify_interface_data(navigation_name_list, driver)
    print(page_block_list)
    # 判断是否有二级导航（1、增加二级导航判断，确定当前频道页名称）
    if navigation_name_list[-1] == '':
        channel_name = navigation_name_list[0]
    else:
        channel_name = navigation_name_list[-1]

    try:

        len_page_block_list = len(page_block_list)
        logging.info(channel_name+'频道共有区块%s个' % len_page_block_list)

        # 2、遍历页面区块的数量
        for block_num in range(len_page_block_list):
            block_num = block_num+1  # 页面区块编号
            len_page_block_list = len(page_block_list[block_num])
            # 接口的页面信息列表中，判断每个区块信息是否为列表            # 判断接口返回的区块信息是否符合要求
            if len_page_block_list >= 1:
                # 获取区块名称
                block_no_name = page_block_list[block_num][0]
                logging.info('------%s频道页第%s个区块：%s------' % (channel_name, block_num, block_no_name))

                # 3、生成当前区块的推荐位元素控件id
                list_block_number = pageBlockID.page_block_id(block_no_name)
                print(list_block_number)  # 20190617修改

                # len_block_recommend_id_list = len(block_recommend_id_list)  # 区块推荐位列表长度决定焦点移动次数

                if len_page_block_list == 1:  # 该区块内无测试推荐位，直接移动焦点
                    blockRecomendTravel.block_recommend_travel_no_target(driver, list_block_number,
                                                                         block_no_name)

                elif len_page_block_list > 1:  # 区块内有要测试的推荐位
                    # 接口返回信息：除区块名称之外的推荐位内容列表
                    block_no_content_list = page_block_list[block_num][1:]
                    logging.info(block_no_content_list)
                    blockRecomendTravel.block_recommend_travel_have_target(driver, list_block_number,
                                                                           block_no_name, block_no_content_list)

    except Exception as e:
        logging.error(e)
