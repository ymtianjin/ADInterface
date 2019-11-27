# encoding=utf-8
import logging
from channel import blockFocusMoveSub

from util import focusMove


def page_block_focus_move(driver, block_num, recommended_num):
    """
    根据区块号确定区块内焦点在推荐位上的移动方向
    :param driver: 
    :param block_num: 区块号
    :param recommended_num: 推荐位号
    :return: 
    """
    if block_num == '001':
        logging.info('001')
        blockFocusMoveSub.block_1_play_focus_move(driver, recommended_num)
    elif block_num == '002' or block_num == '023' or block_num == '028':
        logging.info('002 or 023 or 028')
        blockFocusMoveSub.block_2_23_28_play_focus_move(driver, recommended_num)
    elif block_num == '003' or block_num == '026':
        logging.info('003 or 026')
        blockFocusMoveSub.block_3_26_play_focus_move(driver, recommended_num)
    elif block_num == '004' or block_num == '011':
        logging.info('004 or 011')
        blockFocusMoveSub.block_4_11_play_focus_move(driver, recommended_num)
    elif block_num == '005' or block_num == '008' or block_num == '025':
        logging.info('005 or 008 or 025')
        blockFocusMoveSub.block_8_5_25_play_focus_move(driver, recommended_num)
    elif block_num == '006' or block_num == '007' or block_num == '024':
        logging.info('006 or 007 or 024')
        blockFocusMoveSub.block_6_7_24_play_focus_move(driver, recommended_num)
    elif block_num == '009':
        logging.info('009')
        blockFocusMoveSub.block_9_play_focus_move(driver, recommended_num)
    elif block_num == '010':
        logging.info('010')
        blockFocusMoveSub.block_10_play_focus_move(driver, recommended_num)
    elif block_num == '012':
        logging.info('012')
        blockFocusMoveSub.block_12_play_focus_move(driver, recommended_num)
    elif block_num == '013':
        logging.info('013')
        blockFocusMoveSub.block_13_play_focus_move(driver, recommended_num)
    elif block_num == '014':
        logging.info('014')
        blockFocusMoveSub.block_14_play_focus_move(driver, recommended_num)
    elif block_num == '015':
        logging.info('015')
        blockFocusMoveSub.block_15_play_focus_move(driver, recommended_num)
    elif block_num == '016':
        logging.info('016')
        blockFocusMoveSub.block_16_play_focus_move(driver, recommended_num)
    elif block_num == '017':
        logging.info('017')
        blockFocusMoveSub.block_17_play_focus_move(driver, recommended_num)
    elif block_num == '018':
        logging.info('018')
        blockFocusMoveSub.block_18_play_focus_move(driver, recommended_num)
    elif block_num == '019':
        logging.info('019')
        blockFocusMoveSub.block_19_play_focus_move(driver, recommended_num)
    elif block_num == '020':
        logging.info('not found num 20')
    elif block_num == '021':
        logging.info('021')
        blockFocusMoveSub.block_21_play_focus_move(driver, recommended_num)
    elif block_num == '022':
        logging.info('022')
        blockFocusMoveSub.block_22_play_focus_move(driver, recommended_num)
    elif block_num == '027':
        logging.info('027')
        blockFocusMoveSub.block_27_play_focus_move(driver, recommended_num)
    elif block_num == '029':
        logging.info('029')
        blockFocusMoveSub.block_29_play_focus_move(driver, recommended_num)
    elif block_num == '030':
        logging.info('030')
        blockFocusMoveSub.block_30_play_focus_move(driver, recommended_num)
    elif block_num == '031':
        logging.info('031')
        blockFocusMoveSub.block_31_play_focus_move(driver, recommended_num)
    elif block_num == '032':
        logging.info('not found num 32')


def page_block_focus_move_return(driver, block_num):
    """
    '''
    根据区块号确定区块内推荐位焦点的返回，将焦点移动到区块的最左侧
    :param driver:
    :param block_num: 区块号
    :return:
    """
    if block_num == '001':
        pass

    elif block_num in ['002', '023', '028']:
        # 左移1次
        focusMove.move_direction(driver, 1, 21)
        logging.info('左移1次')

    elif block_num in ['003', '009', '012', '026']:
        # 左移2次
        focusMove.move_direction(driver, 2, 21)
        logging.info('左移2次')

    elif block_num in['004', '010', '011', '013', '015', '016', '017', '019', '027', '031']:
        # 左移3次
        focusMove.move_direction(driver, 3, 21)
        logging.info('左移3次')

    elif block_num in['005', '008', '021', '025', '029', '030']:
        # 左移5次
        focusMove.move_direction(driver, 5, 21)
        logging.info('左移5次')

    elif block_num in['006', '007', '024']:
        # 左移7次
        focusMove.move_direction(driver, 7, 21)
        logging.info('左移7次')

    elif block_num == '014':
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('下移1次')
        # 左移2次
        focusMove.move_direction(driver, 2, 21)
        logging.info('左移2次')

    elif block_num == '018':
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('下移1次')
        # 左移1次
        focusMove.move_direction(driver, 1, 21)
        logging.info('左移1次')

    elif block_num == '020':
        logging.info('not 20')

    elif block_num == '022':
        # 左移4次
        focusMove.move_direction(driver, 4, 21)
        logging.info('左移4次')

    elif block_num == '032':
        logging.info('not found num 32')
