# encoding=utf-8
import json, requests

class Parser:
    def __init__(self):
        self.indexUrl = "http://111.32.138.57:81/api/v31/8acb5c18e56c1988723297b1a8dc9260/600001/navigation/index.json"
        self.pageUrl = "http://testcms31.ottcn.com:30013/api/v31/8acb5c18e56c1988723297b1a8dc9260/600001/page/{page_id}.json"
        self.contentUrl = "http://testcms31.ottcn.com:30013/api/v31/8acb5c18e56c1988723297b1a8dc9260/600001/content/{left_content}/{right_content}/{content_id}.json"
        self.menuUrl = "http://111.32.138.57:81/api/v31/8acb5c18e56c1988723297b1a8dc9260/600001/categorytree/categorytree.json"
        self.program = {}
        self.menu = {}

    def index(self):
        try:
            res = requests.get(url=self.indexUrl)
            if res.status_code != 200:
                return False
            data = json.loads(res.text)
            if not isinstance(data, dict):
                return False
            if data.errorCode != 200:
                return False
            if not isinstance(data.data, list):
                return False
        except BaseException:
            return False
        self.program = {
            "data": [],
            "errorMessage": data.errorMessage,
            "errorCode": data.errorCode
        }
        for levelOneChannel in data.data:
            pageId = levelOneChannel.id
            pageData = self.page(pageId)
            if isinstance(pageData, dict) and len(pageData) > 0:
                levelOneChannel["page"] = pageData
            childChannel = []
            if isinstance(levelOneChannel.child, list):
                for levelTwoChannel in levelOneChannel.child:
                    pageId = levelTwoChannel.id
                    pageData = self.page(pageId)
                    if not pageData:
                        continue
                    levelTwoChannel["page"] = pageData
                    childChannel.append(levelTwoChannel)
            levelOneChannel["child"] = childChannel
            self.program.data.append(levelOneChannel)

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
            if data.errorCode != 200:
                return False
            if not isinstance(data.data, list):
                return False
            if not isinstance(data.logo, str) or len(data.logo) > 0:
                return False
            pageData = {
                "data": [],
                "isNav": data.isNav,
                "subTitle": data.subTitle,
                "pageTitle": data.pageTitle,
                "background": data.background,
                "errorMessage": data.errorMessage,
                "errorCode": data.errorCode,
                "logo": data.logo,
                "description": data.description,
                "titlePoster": data.titlePoster,
                "isAd": data.isAd,
                "templateZT": data.templateZT
            }
            for blockData in data.data:
                programs = []
                if isinstance(blockData.programs, list):
                    for programData in blockData.programs:
                        if programData.l_actionType != "OPEN_DETAILS":
                            continue
                        if programData.contentType != "PS" and programData.contentType != "CS" and programData.contentType != "TV":
                            continue
                        contentId = programData.contentId
                        content = self.content(contentId)
                        if not content:
                            continue
                        programs.append(content)
                blockData["programs"] = programs
                pageData.data.append(blockData)
            if len(pageData.data) == 0:
                return False
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
            if data.errorCode != 200:
                return False
            if not isinstance(data, dict) or len(data.data) < 3:
                return False
            if data.vipFlag == 0 or data.vipFlag is None:
                return False
            contentData = data
            return contentData
        except BaseException:
            return False

    def menu(self):
        try:
            res = requests.get(url=self.menuUrl)
            if res.status_code != 200:
                return False
            data = json.loads(res.text)
            if not isinstance(data, dict):
                return False
            if data.errorCode != 200:
                return False
            if not isinstance(data.data, list):
                return False
            self.menu = data
        except BaseException:
            return False

