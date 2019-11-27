from cases import paramAndPlay
# encoding=utf-8
from channel import blockFocusMove
from util import focusMove,locateElement,const
import logging


def block_recommend_travel_no_target(driver, len_block_recommend_id_list, block_no_name):
    """
    无测试推荐位的区块遍历
    :param driver:
    :param len_block_recommend_id_list:
    :param block_no_name:区块名称
    :return:
    """
    for block_recommend_no in range(len_block_recommend_id_list):  # 遍历区块推荐位并移动焦点，根据步骤3
        block_recommend_num = block_recommend_no+1
        logging.info('当前区块%s的第%s个位置' % (block_no_name, block_recommend_num))
        blockFocusMove.page_block_focus_move(driver, block_no_name, block_recommend_no)  # 根据区块名称，推荐位编号移动焦点
    blockFocusMove.page_block_focus_move_return(driver, block_no_name)  # 恢复区块焦点
    focusMove.move_direction(driver, 1, 20)  # 焦点移动到下一区块


def interface_travel(driver, block_no_content_list, block_recommend_no):
    """
    遍历接口与当前遍历推荐位对比
    :param driver:
    :param block_no_content_list:
    :param block_recommend_no: 推荐位编号
    :return:
    """
    # 遍历接口信息：需要测试的推荐位内容
    for content_dict_no in range(len(block_no_content_list)):
        print(content_dict_no)
        print(block_no_content_list[content_dict_no])  # 每一个推荐位内容为字典格式
        if block_recommend_no in block_no_content_list[content_dict_no].keys():
            content_num = str(content_dict_no+1)  # 匹配上的推荐位的第几个
            print(content_num)
            content_type = block_no_content_list[content_dict_no][block_recommend_no][0]  # 推荐位的详情页类型
            detail_page_title = block_no_content_list[content_dict_no][block_recommend_no][1]  # 推荐位的详情页名称
            print('---------------点击推荐位进入详情页并返回-----------', content_type, detail_page_title, content_num)

            # 调用用例方法，运行对应用例
            obj = paramAndPlay.ParamAndPlay()
            obj.verify(driver, content_type, content_num)

            # 判断当前页面是否为频道页
            while True:
                try:
                    if locateElement.find_element(driver, const.Const.first_class_xpath):
                        break
                except Exception as e:
                    print(e)
                    focusMove.move_direction(driver, 1, 4)

            break


def block_recommend_travel_have_target(driver, len_block_recommend_id_list, block_no_name, block_no_content_list):
    """
    有测试推荐位的区块遍历
    :param driver:
    :param len_block_recommend_id_list:
    :param block_no_name:
    :param block_no_content_list:
    :return:
    """
    # 遍历当前区块推荐位
    for block_recommend_no in range(len_block_recommend_id_list):
        block_recommend_num = block_recommend_no+1  # 遍历数从0开始，为了显示数量从1开始计数
        logging.info('当前区块%s的第%s个位置' % (block_no_name, block_recommend_num))

        # 遍历接口信息：需要测试的推荐位内容
        interface_travel(driver, block_no_content_list, block_recommend_no)

        # 根据区块名称，推荐位编号移动焦点
        blockFocusMove.page_block_focus_move(driver, block_no_name, block_recommend_no)
    # 2.6、区块推荐位遍历完成恢复区块焦点位置
    blockFocusMove.page_block_focus_move_return(driver, block_no_name)

    # 向下移动焦点
    focusMove.move_direction(driver, 1, 20)
