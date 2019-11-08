# encoding=utf-8
import json, requests

class Parser:
    def __init__(self):
        self.indexUrl = "http://111.32.138.57:81/api/v31/8acb5c18e56c1988723297b1a8dc9260/600001/navigation/index.json"
        self.pageUrl = "http://testcms31.ottcn.com:30013/api/v31/8acb5c18e56c1988723297b1a8dc9260/600001/page/{page_id}.json"
        self.contentUrl = "http://testcms31.ottcn.com:30013/api/v31/8acb5c18e56c1988723297b1a8dc9260/600001/content/{left_content}/{right_content}/{content_id}.json"
        self.program = {}

    def index(self):
        try:
            res = requests.get(url=self.indexUrl)
            if res.status_code != 200:
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
        try:
            url = self.pageUrl
            url.replace("{page_id}", pageId)
            res = requests.get(url=url)
            if res.status_code != 200:
                return False
            data = json.loads(res.text)
            if not isinstance(data, dict):
                return False
            if not isinstance(data.data, list):
                return False
            pageData = data
            for blockIndex, blockData in enumerate(pageData.data):
                if not isinstance(blockData.programs, list):
                    continue
                for programIndex, programData in enumerate(blockData.programs):
                    contentId = programData.contentId
                    content = self.content(contentId)
                    pageData.data[blockIndex].programs[programIndex]["content"] = content
            return pageData
        except BaseException:
            return False

    def content(self, contentId):
        try:
            url = self.contentUrl
            url.replace("{left_content}", contentId[0, 2])
            url.replace("{right_content}", contentId[len(contentId) - 2, len(contentId)])
            url.replace("{content_id}", contentId)
            res = requests.get(url=url)
            if res.status_code != 200:
                return False
            data = json.loads(res.text)
            if not isinstance(data, dict):
                return False
            contentData = data
            return contentData
        except BaseException:
            return False

    def menu(self):
        pass

