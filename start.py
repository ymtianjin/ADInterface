# encoding=utf-8
import unittest
import logging
import os

from common import Log, HTMLReport
from tests import Uion


#获取start的日志
logger = logging.getLogger('start')
logger.setLevel(logging.DEBUG)

logPath = os.path.join(os.getcwd(), 'results/logs/')
#根节点初始化
log = Log.createMainLog(logPath)
# 打印日志，运行用例
logger.info('begin to generate testcase')

# 执行用例
ts = unittest.TestSuite()
testLoader = unittest.defaultTestLoader
# 投放测试
t1 = testLoader.loadTestsFromModule(Uion)
ts.addTest(t1)

#修改测试

#logPath = os.path.join(os.getcwd(), 'results/report/', time.strftime('%Y%m%d%H%M%S') + 'report.html')
#logFile = open(logPath, 'wb')
#runner = HTMLTestRunner.HTMLTestRunner(stream = logFile, title = '测试报告', description = '测试执行结果：')
#runner.run(ts)
unittest.TextTestRunner(verbosity=2).run(ts)

