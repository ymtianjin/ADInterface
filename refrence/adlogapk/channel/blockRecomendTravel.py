# encoding=utf-8
__author__ = 'lqq'
# 遍历推荐位
from cases import paramAndPlay
from channel import blockFocusMove
from util import focusMove,locateElement,const
import logging







def interface_block_no_content_travel(driver, block_no_content_list, block_recommend_no):
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
        print (content_no)
        if content_no == block_recommend_no:
            content_num = str(content_no+1)
            print(content_num)
            # print('---------------点击推荐位进入详情页并返回-----------', content_type, content_name, content_num)
            print('---------------点击推荐位进入详情页并返回-----------',  content_num)
            # 调用用例方法，运行对应用例
            # paramAndPlay.verify(driver, content_type, content_name)
            paramAndPlay.verify(driver,block_recommend_no,content_num)

            # 判断当前页面是否为频道页
            while True:
                try:
                    if locateElement.find_element(driver, const.Const.first_class_xpath):
                        print ('在频道页移动焦点到下一个推荐位')
                        break
                except Exception as e:
                    print(e)
                    focusMove.move_direction(driver, 1, 4)
            break





def block_recommend_travel_have_target(driver, list_block_number, block_no_name, block_no_content_list):
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
        block_recommend_num = block_recommend_no+1  # 遍历数从0开始，为了显示数量从1开始计数
        logging.info('当前区块%s的第%s个位置' % (block_no_name, block_recommend_num))

        if block_no_content_list == []:
            logging.info('无推荐位遍历')
        elif block_no_content_list != []:
            # 需要测试的推荐位内容
            interface_block_no_content_travel(driver, block_no_content_list, block_recommend_no)

        # print (block_no_name, block_recommend_no)
        # print(type(block_no_name),type(block_recommend_no))
        # 根据区块名称，推荐位编号移动焦点
        blockFocusMove.page_block_focus_move(driver, block_no_name, block_recommend_no)

    # 2.6、区块推荐位遍历完成恢复区块焦点位置
    blockFocusMove.page_block_focus_move_return(driver, block_no_name)
    # 向下移动焦点
    focusMove.move_direction(driver, 1, 20)
