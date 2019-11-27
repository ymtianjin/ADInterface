# encoding=utf-8
import logging
from interface.interfaceEntry import get_json_value


def verify_interface_data(navigation_name_list, driver):
    """
    接收接收数据，并验证接口数据是否符合要求
    返回符合要求的列表，否则返回None
    :param navigation_name_list:
    :param driver:
    :return:
    """
    page_block_list_info = get_json_value(navigation_name_list)
    print(page_block_list_info)

    try:
        if not isinstance(page_block_list_info, list):  # 判断接口返回是否为列表
            logging.error('接口数据不是列表')
            driver.quit()

        if len(page_block_list_info) == 0:
            logging.error("接口数据为空")
            driver.quit()

        for block in page_block_list_info:
            if isinstance(block, list) and len(block) >= 1:  # 判断接口返回的区块是否为列表且长度是否大于等于1
                if not isinstance(block[0], str):  # 判断区块名称是否为字符
                    logging.error('区块名称应为字符')
                    quit()
                for recommend_content in block[1:]:  # 遍历区块内推荐位
                    if not isinstance(recommend_content, dict):  # 判断推荐位是否为字典
                        logging.error("推荐位信息应为字典")
                        quit()
                    for recommend_content_no, recommend_content_value in recommend_content.items():  # 遍历字典
                        if not isinstance(recommend_content_no, int):  # 判断（key）推荐位编号是否为整型
                            logging.error("推荐位位置应为整型")
                            quit()
                        if not isinstance(recommend_content_value, list):  # 判断value是否为列表
                            logging.error("推荐位位置对应的详情页类型及标题应为列表")
                            quit()
                        for name in recommend_content_value:  # 列表内容是否为字符
                            if not isinstance(name, str):
                                logging.error("详情页类型or 标题应为字符")
                                quit()
            else:
                quit()
        return page_block_list_info
    except Exception as e:
        logging.error(e)

# if __name__ == '__main__':
#     navigation_name_list = ['ZWYTEST', '']
#
#     verify_interface_data(navigation_name_list)