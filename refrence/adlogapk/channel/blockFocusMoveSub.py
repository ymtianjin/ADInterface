# encoding=utf-8
__author__ = 'lqq'
# 区块焦点移动
from util import focusMove
import logging


def block_001_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，1号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if not isinstance(i, int):
        return None
    if i == 0:
        logging.info('焦点不移动')


def block_002_023_028_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，2\23\28号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 1:
        logging.info('区块最后一个推荐位')


def block_003_026_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，3\26号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i in [0,1]:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        logging.info('区块最后一个推荐位')


def block_004_011_play_focus_move(driver, i):
    """
     处理区遍历块推荐位时焦点的移动，4\11号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 3:
        logging.info('区块最后一个推荐位')


def block_008_005_025_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，8\5\25号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 3:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 4:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 5:
        logging.info('区块最后一个推荐位')


def block_006_007_024_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，6\7\24号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 3:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 4:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 5:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 6:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 7:
        logging.info('区块最后一个推荐位')


def block_009_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，9号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 1:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 2:
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 3:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 4:
        logging.info('区块最后一个推荐位')


def block_010_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，10号区块
    :param driver:
    :param i:区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 1:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 2:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 3:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 4:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 5:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 6:
        logging.info('区块最后一个推荐位')


def block_012_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，12号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 3:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 4:
        logging.info('区块最后一个推荐位')


def block_013_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，13号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 3:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 4:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 5:
        logging.info('区块最后一个推荐位')


def block_014_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，14号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    ***恢复焦点时多下移一次***
    :return:
    """
    if i == 0:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 1:
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 2:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 3:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 4:
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 5:
        logging.info('区块最后一个推荐位')


def block_015_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，15号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 3:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 4:
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 5:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 6:
        logging.info('区块最后一个推荐位')


def block_016_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，16号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 3:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 4:
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 5:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 6:
        logging.info('区块最后一个推荐位')


def block_017_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，17号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 左移1次
        focusMove.move_direction(driver, 1, 21)
        logging.info('焦点左移1次')
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 3:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 4:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
        # 左移3次
        focusMove.move_direction(driver, 3, 21)
        logging.info('焦点左移3次')
    elif i == 5:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 6:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 7:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 8:
        logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')


def block_018_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，18号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    ***恢复焦点时多下移一次**
    :return:
    """
    if i == 0:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 1:
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 3:
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 4:
        logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')


def block_019_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，19号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 3:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
        # 左移1次
        focusMove.move_direction(driver, 1, 21)
        logging.info('焦点左移1次')
    elif i == 4:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 5:
        logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')


def block_021_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，21号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 左移2次
        focusMove.move_direction(driver, 2, 21)
        logging.info('焦点左移2次')
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 3:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 4:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 5:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 6:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 7:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 8:
        logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')


def block_022_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，22号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 3:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移2次
        focusMove.move_direction(driver, 2, 19)
        logging.info('焦点上移2次')
    elif i == 4:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 5:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 6:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移2次
        focusMove.move_direction(driver, 2, 19)
        logging.info('焦点上移2次')
    elif i == 7:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 8:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 9:
        logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')


def block_027_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，27号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 左移2次
        focusMove.move_direction(driver, 2, 21)
        logging.info('焦点左移2次')
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 3:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 4:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 5:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 6:
        logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')


def block_029_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，29号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
        # 左移1次
        focusMove.move_direction(driver, 1, 21)
        logging.info('焦点左移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 2:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移2次
        focusMove.move_direction(driver, 2, 19)
        logging.info('焦点上移2次')
    elif i == 3:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 4:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
        # 左移1次
        focusMove.move_direction(driver, 1, 21)
        logging.info('焦点左移1次')
    elif i == 5:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 6:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移2次
        focusMove.move_direction(driver, 2, 19)
        logging.info('焦点上移2次')
    elif i == 7:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 8:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
        # 左移1次
        focusMove.move_direction(driver, 1, 21)
        logging.info('焦点左移1次')
    elif i == 9:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 10:
        logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')


def block_030_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，30号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 1:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 2:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 3:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 4:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 5:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 6:

        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 7:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 8:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 9:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 10:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 11:
        logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')


def block_031_play_focus_move(driver, i):
    """
    处理区遍历块推荐位时焦点的移动，31号区块
    :param driver:
    :param i: 区块推荐位列表序列号，即区块的第几个推荐位
    :return:
    """
    if i == 0:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 1:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 2:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 3:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 4:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
        # 上移1次
        focusMove.move_direction(driver, 1, 19)
        logging.info('焦点上移1次')
    elif i == 5:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
    elif i == 6:
        # 下移1次
        focusMove.move_direction(driver, 1, 20)
        logging.info('焦点下移1次')
        # 左移1次
        focusMove.move_direction(driver, 3, 21)
        logging.info('焦点左移3次')
    elif i == 7:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 8:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 9:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 10:
        # 右移1次
        focusMove.move_direction(driver, 1, 22)
        logging.info('焦点右移1次')
    elif i == 11:
        logging.info('左后一个推荐位，焦点需要移动到当前行的第一个位置')
