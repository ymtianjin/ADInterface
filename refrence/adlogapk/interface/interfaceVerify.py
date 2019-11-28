# encoding=utf-8
import logging
__author__ = 'lqq'
# 验证接口数据


# def verify_interface_data(page_block_list_info, driver):
def verify_interface_data(page_block_list_info,driver):
    """
    接收接收数据，并验证接口数据是否符合要求
    返回符合要求的列表，否则返回None
    :param navigation_name_list:
    :param driver:
    :return:
    lqq
    """
    try:
        if not isinstance(page_block_list_info, list):  # 判断接口返回是否为列表
            logging.error('接口数据不是列表')
            driver.quit()

        if len(page_block_list_info) == 0:
            logging.error("接口数据为空")
            driver.quit()

        for block_list in page_block_list_info:
            if isinstance(block_list, list) and len(block_list) >= 1:  # 判断接口返回的区块是否为列表且长度是否大于等于1
                for block_n in range(len(block_list)):
                    if block_n ==0 :
                        if not isinstance(block_list[block_n], str):  # 判断区块名称是否为字符
                            logging.error('区块名称应为字符')
                            quit()
                    elif block_n ==1 :
                        if not isinstance(block_list[block_n],int):# 判断推荐位位置是否为整形
                            logging.error("推荐位信息应为整形")
                            quit()
            else:
                quit()
        return page_block_list_info
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    page_block_list_info = [['004', 0]]

    verify_interface_data(page_block_list_info)