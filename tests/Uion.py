# encoding=utf-8
import unittest, logging
import os

from common import Param, Http

class Uion(unittest.TestCase):
    parentPath = None
    param = None
    http = None

    def setUp(self):
        self.parentPath = os.path.join(os.getcwd(), '/data');
        self.param = Param.Param(self)

        self.http = Http.Http(self)


    def tearDown(self):
        pass


    def test_free(self):
        logging.info(self._testMethodName)

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
                logging.info("case: " + caseName)
                stepIndex = 1
                stepStart = 1
                while True:
                    address = self.param.readStep(stepStart)
                    if address == None:
                        break
                    data = self.param.readData(stepStart)
                    check = self.param.readCheck(stepStart)
                    logging.info("step: " + str(stepIndex) + ", " + str(address))
                    logging.info("data: " + str(data))
                    logging.info("check: " + str(check))
                    for index in range(0, address["count"]):
                        logging.info("execute: " + str(index + 1))
                        if address["method"] == "get":
                            res = self.http.get(address["url"], data, check)
                        elif address["method"] == "post":
                            res = self.http.post(address["url"], data, check)                
                        if not res is None:
                            logging.info(res)
                    stepIndex = stepIndex + 1
                    stepStart = stepStart + max(len(data), len(check)) + 1
                logging.info("===========end============")


if __name__ == '__main__':
    unittest.main()
