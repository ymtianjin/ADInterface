# encoding=utf-8
__author__ = 'lqq'
import logging
# 确定区块数量

def page_block_id(block_no):
    """
    获取推荐位id列表
    :param block_no: 区块号Design by lqq
    :return: 区块id列表Design by lqq
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


