# encoding=utf-8
import time
import logging


def find_element(driver, id_or_xpath, n=40):
    """
    通过id或者xpath定位单个元素
    返回类型单个元素对象
    :param driver: 
    :param id_or_xpath: 
    :param n: 
    :return: 
    """

    for i in range(n):

        try:
            if id_or_xpath.startswith('/'):
                ret = driver.find_element_by_xpath(id_or_xpath)
            else:
                ret = driver.find_element_by_id(id_or_xpath)
            return ret
        except Exception as e:
            time.sleep(0.5)
            print(e)
            continue


def find_elements(driver, id_or_xpath, n=40):
    """
    通过id或者xpath定位元素列表
    返回类型元素列表
    :param driver:
    :param id_or_xpath:
    :param n:
    :return:
    """
    for i in range(n):
        try:
            if id_or_xpath.startswith('/'):
                ret = driver.find_elements_by_xpath(id_or_xpath)
            else:
                ret = driver.find_elements_by_id(id_or_xpath)
            return ret
        except Exception as e:
            time.sleep(0.5)
            print(e)
            continue


def elements_exist(driver, elements):
    """
    判断是否存在播放鉴权或者错误码
    :param driver:驱动
    :param elements:错误码和鉴权失败xpath
    :return: err_name 元素text属性
    """
    err_name = ''
    for element in elements:
        try:
            err_name = driver.find_element_by_xpath(element).text
            break
        except Exception as e:
            print(e)
            continue
    return err_name


def return_proper(driver, element):
    """

    :param driver:驱动
    :param element:页面元素，判断点击返回键后，页面是否正常返回
    :return:
    """

    ele = ''
    try:
        if element.startswith('/'):
            ele = driver.find_elements_by_xpath(element)
        else:
            ele = driver.find_elements_by_id(element)
    except Exception as e:
        print(e)
    return ele



