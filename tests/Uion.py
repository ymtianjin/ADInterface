# encoding=utf-8
import unittest, logging
import os, time, sys

from common import Param, Http, HTMLReport

class Uion(unittest.TestCase):
    parentPath = None
    param = None
    http = None

    def setUp(self):
        self.parentPath = os.path.join(os.getcwd(), 'data');
        self.param = Param.Param(self)

        self.http = Http.Http(self)


    def tearDown(self):
        pass


    def test_free(self):
        logging.info(self._testMethodName)

        reportPath = os.path.join(os.getcwd(), 'results/report/', time.strftime('%Y%m%d%H%M%S') + 'report.html')
        reportFile = open(reportPath, 'wb')
        report = HTMLReport.HTMLReport(stream = reportFile, title = '接口测试报告', description = '接口测试执行结果：')
        results = []

        files = os.listdir(self.parentPath)
        for file in files:
            path = os.path.join(self.parentPath, file)
            ret = False
            if os.path.isfile(path) and os.path.splitext(path)[1] == '.xlsx':
                ret = self.param.reopen(path)
            if not ret:
                continue

            logging.info("suit: " + file)

            caseCount = self.param.caseCount();

            for caseIndex in range(0, caseCount):
                logging.info("===========bengin============")
                caseName = self.param.switchCase(caseIndex)
                result = HTMLReport.HTMLResult(caseName)
                stepIndex = 1
                stepStart = 1
                while True:
                    address = self.param.readStep(stepStart)
                    if address == None:
                        break
                    data = self.param.readData(stepStart)
                    check = self.param.readCheck(stepStart)
                    if address["method"] == "get":
                        self.http.get(address["url"], data, check)
                    elif address["method"] == "post":
                        self.http.post(address["url"], data, check)
                    stepIndex = stepIndex + 1
                    stepStart = stepStart + max(len(data), len(check)) + 1

                    if self.http.success:
                        result.addSuccess(address["name"], self.http.msg)
                    else:
                        result.addFailure(address["name"], self.http.msg)
                results.append(result)

                logging.info("===========end============")

        report.generate(results)
        reportFile.close()

if __name__ == '__main__':
    unittest.main()
