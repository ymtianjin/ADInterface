# encoding=utf-8
import unittest
import logging
import os

from common import Log
from tests import Uion


#获取start的日志
logger = logging.getLogger('start')
logger.setLevel(logging.DEBUG)

path = os.getcwd() + '/results/logs/'
#根节点初始化
log = Log.createMainLog(path)
# 打印日志，运行用例
logger.info('begin to generate testcase')

# 执行用例
ts = unittest.TestSuite()
testLoader = unittest.defaultTestLoader
# 投放测试
t1 = testLoader.loadTestsFromModule(Uion)
ts.addTest(t1)
unittest.TextTestRunner(verbosity=2).run(ts)

