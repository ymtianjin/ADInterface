# encoding=utf-8
__author__ = 'lqq'
# 调用区块焦点移动方式
import logging
from channel import blockFocusMoveSub
from util import focusMove


def page_block_focus_move(driver,block_no_name, block_recommend_no):

    """
    根据区块号确定调用区块的焦点移动函数
    :param driver:
    :param block_num: 区块号
    :param recommended_num: 推荐位号
    :return:
    """
    try:
        block_name_list = ['002_023_028','003_026','004_011','008_005_025','006_007_024']
        for block_name_info in block_name_list:
            if block_no_name in block_name_info:
                method_name = 'blockFocusMoveSub.block_'+block_name_info+'_play_focus_move'
                break
            else:
                continue
        else:
            method_name = 'blockFocusMoveSub.block_'+block_no_name+'_play_focus_move'

        eval(method_name)(driver, block_recommend_no)

    except Exception as e:
        logging.error(e)


def page_block_focus_move_return(driver, block_name):
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
        focusMove.move_direction(driver, 1, 21)
        logging.info('左移1次')

    elif block_name in ['003', '009', '012', '026']:
        # 左移2次
        focusMove.move_direction(driver, 2, 21)
        logging.info('左移2次')

    elif block_name in['004', '010', '011', '013', '015', '016', '017', '019', '027', '031']:
        # 左移3次
        focusMove.move_direction(driver, 3, 21)
        logging.info('左移3次')

    elif block_name in['005', '008', '021', '025', '029', '030']:
        # 左移5次
        focusMove.move_direction(driver, 5, 21)
        logging.info('左移5次')

    elif block_name in['006', '007', '024']:
        # 左移7次
        focusMove.move_direction(driver, 7, 21)
        logging.info('左移7次')

    elif block_name == '014':
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('下移1次')
        # 左移2次
        focusMove.move_direction(driver, 2, 21)
        logging.info('左移2次')

    elif block_name == '018':
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('下移1次')
        # 左移1次
        focusMove.move_direction(driver, 1, 21)
        logging.info('左移1次')

    elif block_name == '020':
        logging.info('not 20')

    elif block_name == '022':
        # 左移4次
        focusMove.move_direction(driver, 4, 21)
        logging.info('左移4次')

    elif block_name == '032':
        logging.info('not found num 32')


