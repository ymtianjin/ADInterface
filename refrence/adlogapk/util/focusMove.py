# encoding=utf-8
import time
import logging


def move_direction(driver, num, direction, duration=0.5):
    """
    焦点移动
    :param driver:
    :param num: 焦点移动次数
    :param direction: 焦点移动方向
    :param duration:
    :return:
    """
    dict_direction = {'19': 'Move up', '20': 'Move down',
                      '21': 'Move left', '22': 'Move right', '23': 'enter', '4': 'return'}
    if not isinstance(num, int) and not isinstance(direction, int) and not isinstance(duration, float):
        return None
    try:
        for i in range(num):
            driver.keyevent(direction)
            time.sleep(duration)
        if str(direction) in dict_direction.keys():
            logging.info(u"%s %s times" % (dict_direction[str(direction)], (i+1)))
            print(u"%s %s次" % (dict_direction[str(direction)], (i+1)))
    except Exception as e:
        logging.error(e)

