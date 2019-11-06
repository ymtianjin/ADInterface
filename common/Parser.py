# encoding=utf-8
import json, requests

class Parser:
    def __init__(self):
        self.indexUrl = "http://111.32.138.57:81/api/v31/8acb5c18e56c1988723297b1a8dc9260/600001/navigation/index.json"
        self.program = {}

    def index(self):
        try:
            res = requests.get(url=self.indexUrl)
            if res.status_code <> 200:
                return False
            data = json.loads(res.text)
            if not isinstance(data, dict):
                return False
            if not isinstance(data.data, list):
                return False
            self.program = data
        except BaseException:
            return False
        for levelOneIndex, levelOneChannel in enumerate(self.program.data):
            pageId = levelOneChannel.id
            pageData = self.page(pageId)
            self.program.data[levelOneIndex]["page"] = pageData;
            if not isinstance(levelOneChannel.child, list):
                continue
            for levelTwoIndex, levelTwoChannel in enumerate(levelOneChannel.child):
                pageId = levelTwoChannel.id
                pageData = self.page(pageId)
                self.program.data[levelOneIndex].child[levelTwoIndex]["page"] = pageData

    def page(self, pageId):
        pass

    def content(self):
        pass

    def menu(self):
        pass

