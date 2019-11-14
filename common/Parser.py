# encoding=utf-8
import json, requests, random

class Parser:
    def __init__(self):
        self.appKey = ""
        self.channelCode = ""
        self.indexUrl = "http://testcms31.ottcn.com:30012/api/v31/{app_key}/{channel_code}/navigation/index.json"
        self.pageUrl = "http://testcms31.ottcn.com:30012/api/v31/{app_key}/{channel_code}/page/{page_id}.json"
        self.contentUrl = "http://testcms31.ottcn.com:30012/api/v31/{app_key}/{channel_code}/content/{left_content}/{right_content}/{content_id}.json"
        self.subcontentUrl = "http://testcms31.ottcn.com:30012/api/v31/{app_key}/{channel_code}/detailsubcontents/{content_id}.json?subcontenttype=subcontents"
        self.categoryTreeUrl = "http://testcms31.ottcn.com:30012/api/v31/{app_key}/{channel_code}/categorytree/categorytree.json"
        self.channel = {}
        self.program = []
        self.category = {}

    def index(self):
        try:
            url = self.indexUrl
            url = url.replace("{app_key}", self.appKey)
            url = url.replace("{channel_code}", self.channelCode)
            res = requests.get(url=url)
            if res.status_code != 200:
                return False
            data = json.loads(res.text)
            if not isinstance(data, dict):
                return False
            if data["errorCode"] != "0":
                return False
            if not isinstance(data["data"], list):
                return False
        except BaseException:
            return False
        self.channel = {
            "data": [],
            "errorMessage": data.errorMessage,
            "errorCode": data.errorCode
        }
        for levelOneChannel in data.data:
            levelOneClickParam = {
                "levelOneId": lenvelOneChannel.id,
                "levelOne": lenvelOneChannel.title
            }
            pageId = levelOneChannel.id
            pageData = self.page(pageId, levelOneClickParam)
            if isinstance(pageData, dict) and len(pageData) > 0:
                levelOneChannel["page"] = pageData
            childChannel = []
            if isinstance(levelOneChannel.child, list):
                for levelTwoChannel in levelOneChannel.child:
                    levelTwoClickParam = levelOneClickParam
                    levelTwoClickParam["levelTwoId"] = levelTwoChannel.id
                    levelTwoClickParam["levelTwo"] = levelTwoChannel.title
                    pageId = levelTwoChannel.id
                    pageData = self.page(pageId, levelTwoClickParam)
                    if not pageData:
                        continue
                    levelTwoChannel["page"] = pageData
                    childChannel.append(levelTwoChannel)
            levelOneChannel["child"] = childChannel
            self.channel.data.append(levelOneChannel)

    def page(self, pageId, clickParam):
        try:
            url = self.pageUrl
            url.replace("{app_key}", self.appKey)
            url.replace("{channel_code}", self.channelCode)
            url.replace("{page_id}", pageId)
            res = requests.get(url=url)
            if res.status_code != 200:
                return False
            data = json.loads(res.text)
            if not isinstance(data, dict):
                return False
            if data.errorCode != "0":
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
                "isAd": data.isAd,
                "templateZT": data.templateZT
            }
            clickParam["block"] = []
            for blockData in data.data:
                layoutCode = blockData.layoutCode
                clickParam.block.append(layoutCode[len(layoutCode) - 3, len(layoutCode)])
                programs = []
                if isinstance(blockData.programs, list):
                    for programIndex, programData in enumerate(blockData.programs):
                        if programData.l_actionType != "OPEN_DETAILS":
                            continue
                        if programData.contentType != "PS" and programData.contentType != "CS" and programData.contentType != "TV": #节目集类型：CS=合集、TV=电视、PS=剧集
                            continue
                        contentId = programData.contentId
                        content = self.content(contentId, clickParam, programIndex)
                        if not content:
                            continue
                        programData["content"] = content
                        programs.append(programData)
                if len(programs) == 0:
                    continue
                blockData["programs"] = programs
                pageData.data.append(blockData)
            if len(pageData.data) == 0:
                return False
            return pageData
        except BaseException:
            return False

    def content(self, contentId, clickParam, programIndex):
        try:
            url = self.contentUrl
            url.replace("{app_key}", self.appKey)
            url.replace("{channel_code", self.channelCode)
            url.replace("{left_content}", contentId[0, 2])
            url.replace("{right_content}", contentId[len(contentId) - 2, len(contentId)])
            url.replace("{content_id}", contentId)
            res = requests.get(url=url)
            if res.status_code != 200:
                return False
            data = json.loads(res.text)
            if not isinstance(data, dict):
                return False
            if data.errorCode != "0":
                return False
            if data.data.vipFlag == "0" or data.data.vipFlag is None:
                return False

            if data.data.contentType == "CS" and data.data.seriesType == "1": #当contentType为CS的时候，seriesType为1表示剧集（需要获取subcontent），如果seriesType为0表示综艺
                url = self.subcontentUrl
                url.replace("{content_id}", contentId)
                res = requests.get(url=url)
                if res.status_code != 200:
                    return False
                subcontentData = json.loads(res.text)
                if not isinstance(subcontentData, dict):
                    return False
                if subcontentData.errorCode != "0":
                    return False
                if not isinstance(subcontentData.data, list) or len(subcontentData.data) < 3:
                    return False
                data["subcontent"] = subcontentData

            contentData = data

            #构造点击参数字符串：['CCTV+','CCTV5',[['017'],['005'],['008',3]]]
            param = []
            param.append(clickParam.levelOne)
            if clickParam.has_key("levelTwo"):
                param.append(clickParam.levelTwo)
            else:
                param.append("")
            block = []
            for blockLayout in clickParam.block:
                layout = [blockLayout]
                block.append(layout)
            block[len(block) - 1].append(programIndex)
            param.append(block)
            contentData["clickParam"] = param

            categoryIds = contentData.categoryIDs.split("|")
            category = {"levelOne": [], "levelTwo": categoryIds}
            for categoryId in categoryIds:
                if self.category.has_key(categoryId):
                    category.levelOne.append(self.category[categoryId])
            contentData["category"] = category

            self.program.append(contentData)

            return contentData
        except BaseException:
            return False

    def categoryTree(self):
        try:
            url = self.categoryTreeUrl
            url.replace("{app_key}", self.appKey)
            url.replace("{channel_code}", self.channelCode)
            res = requests.get(url=url)
            if res.status_code != 200:
                return False
            data = json.loads(res.text)
            if not isinstance(data, dict):
                return False
            if data.errorCode != "0":
                return False
            if not isinstance(data.data, list):
                return False

            self.category = {}
            for levelOneCategoryData in data.data:
                if isinstance(levelOneCategoryData.child, list):
                    for levelTwoCategoryData in levelOneCategoryData.child:
                        self.category[levelTwoCategoryData.id] = levelOneCategoryData.id

        except BaseException:
            return False

    def appChannel(self, appKey, channelCode):
        self.appKey = appKey
        self.channelCode = channelCode

    def filter(self, duration = 0, levelOneChannel = [], levelTwoChannel = [], videoType = [], videoClass = [], levelOneCategory = [], levelTwoCategory = [], series = []):
        self.channel = {}
        self.program = []
        self.menu = {}
        self.category = {}

        self.categoryTree()
        self.index()

        if len(self.program) == 0:
            return ""
        ps = []
        tv = []
        cs = []
        csSeries = []
        for programData in self.program:
            if isinstance(duration, int) and duration > 0 and int(programData.duration) < duration: #过滤时长
                continue
            if isinstance(levelOneChannel, list) and len(levelOneChannel) > 0 and programData.clickParam.levelOneChannelId not in levelOneChannel:
                continue
            if isinstance(levelTwoChannel, list) and len(levelTwoChannel) > 0 and programData.clickParam.levelTwoChannelId not in levelTwoChannel:
                continue
            if isinstance(videoType, list) and len(videoType) > 0 and programData.videoType not in videoType:
                continue
            if isinstance(videoClass, list) and len(videoClass) > 0 and programData.videoClass not in videoClass:
                continue
            if isinstance(levelOneCategory, list) and len(levelOneCategory):
                bFound = False
                for categoryId in programData.category.levelOne:
                    if categoryId in levelOneCategory:
                        bFound = True
                        break
                if not bFound:
                    continue
            if isinstance(levelTwoCategory, list) and len(levelTwoCategory) > 0:
                bFound = False
                for categoryId in programData.category.levelTwo:
                    if categoryId in levelTwoCategory:
                        bFound = True
                        break
                if not bFound:
                    continue
            if isinstance(series, list) and len(series) > 0:
                if not isinstance(programData.subcontent, dict) or not isinstance(programData.subcontent.data, list) or len(programData.subcontent.data) == 0:
                    continue
                bFound = False
                for subContent in programData.subcontent:
                    if subContent.contentId in series:
                        bFound = True
                        break
                if not bFound:
                    continue
            if programData.contentType == "PS":
                ps.append(programData.clickParam)
            elif programData.contentType == "TV":
                tv.append(programData.clickParam)
            elif programData.contentType == "CS":
                if programData.seriesType == "1":
                    csSeries.append(programData.clickParam)
                else:
                    cs.append(programData.clickParam)
        psParam = ramdon.choice(ps)
        tvParam = ramdon.choice(tv)
        csParam = ramdon.choice(cs)
        csSeriesParam = ramdon.choice(csSeries)

        return [str(psParam), str(tvParam), str(csParam), str(csSeriesParam)]