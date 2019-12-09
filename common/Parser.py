# encoding=utf-8
__author__ = 'limeng'
import json, requests, random, os, logging

class Parser:
    def __init__(self):
        self.FILTER = True
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

        self.parentPath = os.path.join(os.getcwd(), "data")

    def index(self):    #生成channel文件，program文件，遍历导航接口，插入数据
        try:
            path = os.path.join(self.parentPath, "channel.json")   #新建channel.json，program。json文件
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.channel = data
            path = os.path.join(self.parentPath, "program.json")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.program = data

            if len(self.channel) > 0 and len(self.program) > 0:  #判断文件是否存在
                return True

            url = self.indexUrl  #发送http请求接口index并进行判断
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
        except BaseException as e:
            logging.error(e)
            return False
        self.channel = {   #定义channel格式
            "data": [],
            "errorMessage": data["errorMessage"],
            "errorCode": data["errorCode"]
        }
        for levelOneChannel in data["data"]:  #遍历data的data数据，为levelOneChannel
            if self.FILTER and (not isinstance(levelOneChannel["focusIcon"], str) or len(levelOneChannel["focusIcon"]) > 0):  #levelOneChannel的focusIcon不为str 或长度>0，继续下一个遍历
                continue
            levelOneClickParam = {    #构造点击参数，取出id和titile
                "levelOneId": levelOneChannel["id"],
                "levelOne": levelOneChannel["title"]
            }
            if not isinstance(levelOneChannel["child"], list) or len(levelOneChannel["child"]) == 0:
                pageId = levelOneChannel["id"]  #id赋值给pageId
                pageData = self.page(pageId, levelOneClickParam)  #oageData为
                if isinstance(pageData, dict) and len(pageData) > 0:  #判断类型及长度
                    levelOneChannel["page"] = pageData  #pageDate赋值给
            childChannel = []
            if isinstance(levelOneChannel["child"], list):   #child为列表
                for levelTwoChannel in levelOneChannel["child"]:  #遍历data下child
                    if self.FILTER and (not isinstance(levelTwoChannel["focusIcon"], str) or len(levelTwoChannel["focusIcon"]) > 0):  #g过滤焦点图片
                        continue
                    levelTwoClickParam = levelOneClickParam  #将id和title赋值给levelTwoClickParam
                    levelTwoClickParam["levelTwoId"] = levelTwoChannel["id"]
                    levelTwoClickParam["levelTwo"] = levelTwoChannel["title"]  #
                    pageId = levelTwoChannel["id"]  #将child下 的id赋值给pageId
                    pageData = self.page(pageId, levelTwoClickParam)
                    if self.FILTER and not pageData:
                        continue
                    levelTwoChannel["page"] = pageData  #将child下的page赋值给pageData
                    childChannel.append(levelTwoChannel)  #将childChannel下添加child
            levelOneChannel["child"] = childChannel  #childChannel = data下的child
            self.channel["data"].append(levelOneChannel)  #将levelOneChannel添加至channel的data下

        path = os.path.join(self.parentPath, "channel.json")  #拼接channel路径
        with open(path, 'w', encoding='utf-8') as f:  #
            f.write(json.dumps(self.channel, ensure_ascii=False))  #输出真正的中文

        path = os.path.join(self.parentPath, "program.json")  #
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.program, ensure_ascii=False))

        return True


#遍历页面接口，
    def page(self, pageId, clickParam):
        try:
            url = self.pageUrl
            url = url.replace("{app_key}", self.appKey)
            url = url.replace("{channel_code}", self.channelCode)
            url = url.replace("{page_id}", pageId)
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
            # if not isinstance(data["logo"], str) or len(data["logo"]) > 0:
            #    return False
            pageData = {
                "data": [],
                "isNav": data["isNav"],
                "subTitle": data["subTitle"],
                "pageTitle": data["pageTitle"],
                "background": data["background"],
                "errorMessage": data["errorMessage"],
                "errorCode": data["errorCode"],
                "logo": data["logo"],
                "description": data["description"],
                "isAd": data["isAd"],
                "templateZT": data["templateZT"]
            }
            clickParam["block"] = []  #d定义空的点击参数中的block
            for blockData in data["data"]:   #遍历data中的data，
                layoutCode = blockData["layoutCode"]  #取出layout后三位赋值给blockId
                blockId = layoutCode[-3 : ]
                if blockId in ["009", "010", "032"]:
                    return False
                clickParam["block"].append(blockId)
                programs = []
                if isinstance(blockData["programs"], list):  #判断programs类型
                    for programIndex, programData in enumerate(blockData["programs"]):  #遍历programs下的data，加索引
                        if self.FILTER and programData["l_actionType"] != "OPEN_DETAILS":
                            continue
                        if self.FILTER and programData["contentType"] not in ["PS", "CS", "TV", "CG"]: #节目集类型：CS=合集、TV=电视、PS=剧集、CG=节目合集
                            continue
                        contentId = programData["contentId"]  #取出contentId
                        content = self.content(contentId, clickParam, programIndex)   #contet由contentId，
                        if self.FILTER and not content:
                            continue
                        if blockId == "008" and content["data"]["blockType"] == 0:
                            return False
                        programData["content"] = content
                        programs.append(programData)
                if self.FILTER and len(programs) == 0:
                    continue
                blockData["programs"] = programs
                pageData["data"].append(blockData)
            if self.FILTER and len(pageData["data"]) == 0:
                return False
            return pageData
        except BaseException as e:
            logging.error(e)
            return False

    #遍历内容接口
    def content(self, contentId, clickParam, programIndex):
        try:
            url = self.contentUrl
            url = url.replace("{app_key}", self.appKey)
            url = url.replace("{channel_code}", self.channelCode)
            url = url.replace("{left_content}", contentId[0 : 2])
            url = url.replace("{right_content}", contentId[-2 : ])
            url = url.replace("{content_id}", contentId)
            res = requests.get(url=url)
            if res.status_code != 200:
                return False
            data = json.loads(res.text)
            if not isinstance(data, dict):
                return False
            if data["errorCode"] != "0":
                return False
            if self.FILTER and data["data"].__contains__("vipFlag") and data["data"]["vipFlag"] != "0" and data["data"]["vipFlag"] is not None:
                return False

            if data["data"]["contentType"] == "PS" and data["data"]["seriesType"] == "1": #当contentType为CS的时候，seriesType为1表示剧集（需要获取subcontent），如果seriesType为0表示综艺
                url = self.subcontentUrl
                url = url.replace("{app_key}", self.appKey)
                url = url.replace("{channel_code}", self.channelCode)
                url = url.replace("{content_id}", contentId)
                res = requests.get(url=url)
                if res.status_code != 200:
                    return False
                subcontentData = json.loads(res.text)
                if not isinstance(subcontentData, dict):
                    return False
                if subcontentData["errorCode"] != "0":
                    return False
                if self.FILTER and (not isinstance(subcontentData["data"], list) or len(subcontentData["data"]) < 3):
                    return False
                data["subcontent"] = subcontentData

            contentData = data

            #构造点击参数字符串：['CCTV+','CCTV5',[['017'],['005'],['008',3]]]
            channel = {"levelOne": clickParam["levelOneId"], "levelTwo": ""}
            param = []
            param.append(clickParam["levelOne"])
            if "levelTwo" in clickParam:
                param.append(clickParam["levelTwo"])
                channel["levelTwo"] = clickParam["levelTwoId"]
            else:
                param.append("")
            block = []
            for blockLayout in clickParam["block"]:
                layout = [blockLayout]   #layout添加进参数
                block.append(layout)
            block[len(block) - 1].append(programIndex)   #将位置长度-1添加进block
            param.append(block)
            contentData["clickParam"] = param
            contentData["channel"] = channel

            categoryIds = contentData["data"]["categoryIDs"].split("|")  #分隔categoryIds
            category = {"levelOne": [], "levelTwo": categoryIds}
            for categoryId in categoryIds:
                if categoryId in self.category:
                    category["levelOne"].append(self.category[categoryId])
            contentData["category"] = category

            self.program.append(contentData)

            return contentData
        except BaseException as e:
            logging.error(e)
            return False

    #遍历栏目树接口
    def categoryTree(self):
        try:
            path = os.path.join(self.parentPath, "category.json")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.category = data
                        return True

            url = self.categoryTreeUrl
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

            self.category = {}
            for levelOneCategoryData in data["data"]:
                if isinstance(levelOneCategoryData["child"], list):
                    for levelTwoCategoryData in levelOneCategoryData["child"]:
                        self.category[levelTwoCategoryData["id"]] = levelOneCategoryData["id"]

            path = os.path.join(self.parentPath, "category.json")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(self.category, ensure_ascii=False))

            return True
        except BaseException as e:
            logging.error(e)
            return False

    #定义应用渠道
    def appChannel(self, appKey, channelCode):
        self.appKey = appKey
        self.channelCode = channelCode

    #过滤函数
    def filter(self, params):
        if params.__contains__("position") and isinstance(params["position"], list) and len(params["position"]) > 0:
            return [params["position"]]

        self.channel = {}
        self.program = []
        self.menu = {}
        self.category = {}

        self.categoryTree()
        self.index()

        if len(self.program) == 0:
            return []
        ps = []
        psSeries = []
        tv = []
        cs = []
        cg = []
        for programData in self.program:
            if params.__contains__("duration") and isinstance(params["duration"], int) and params["duration"] > 0 and int(programData["data"]["duration"]) < params["duration"]: #过滤时长
                continue
            if params.__contains__("levelOneChannel") and isinstance(params["levelOneChannel"], list) and len(params["levelOneChannel"]) > 0 and programData["channel"]["levelOne"] not in params["levelOneChannel"]:
                continue
            if params.__contains__("levelTwoChannel") and isinstance(params["levelTwoChannel"], list) and len(params["levelTwoChannel"]) > 0 and programData["channel"]["levelTwo"] not in params["levelTwoChannel"]:
                continue
            if params.__contains__("videoType") and isinstance(params["videoType"], list) and len(params["videoType"]) > 0 and programData["data"]["videoType"] not in params["videoType"]:
                continue
            if params.__contains__("videoClass") and isinstance(params["videoClass"], list) and len(params["videoClass"]) > 0 and programData["data"]["videoClass"] not in params["videoClass"]:
                continue
            if params.__contains__("levelOneCategory") and isinstance(params["levelOneCategory"], list) and len(params["levelOneCategory"]):
                bFound = False
                for categoryId in programData["category"]["levelOne"]:
                    if categoryId in params["levelOneCategory"]:
                        bFound = True
                        break
                if not bFound:
                    continue
            if params.__contains__("levelTwoCategory") and isinstance(params["levelTwoCategory"], list) and len(params["levelTwoCategory"]) > 0:
                bFound = False
                for categoryId in programData["category"]["levelTwo"]:
                    if categoryId in params["levelTwoCategory"]:
                        bFound = True
                        break
                if not bFound:
                    continue
            if params.__contains__("series") and isinstance(params["series"], list) and len(params["series"]) > 0:
                if not programData.__contains__("subcontent") or not isinstance(programData["subcontent"], dict) or not isinstance(programData["subcontent"]["data"], list) or len(programData["subcontent"]["data"]) == 0:
                    continue
                bFound = False
                for subContent in programData["subcontent"]["data"]:
                    if subContent["contentId"] in params["series"]:
                        bFound = True
                        break
                if not bFound:
                    continue
            if programData["data"]["contentType"] == "PS":
                if programData["data"]["seriesType"] == "1":
                    psSeries.append(programData["clickParam"])
                else:
                    ps.append(programData["clickParam"])
            elif programData["data"]["contentType"] == "TV":
                tv.append(programData["clickParam"])
            elif programData["data"]["contentType"] == "CS":
                cs.append(programData["clickParam"])
            elif programData["data"]["contentType"] == "CG":
                cg.append(programData["clickParam"])

        if isinstance(ps, list) and len(ps) > 0:
            psParam = random.choice(ps)
        else:
            psParam = []
        if isinstance(tv, list) and len(tv) > 0:
            tvParam = random.choice(tv)
        else:
            tvParam = []
        if isinstance(cs, list) and len(cs) > 0:
            csParam = random.choice(cs)
        else:
            csParam = []
        if isinstance(psSeries, list) and len(psSeries) > 0:
            psSeriesParam = random.choice(psSeries)
        else:
            psSeriesParam = []
        if isinstance(cg, list) and len(cg) > 0:
            cgParam = random.choice(cg)
        else:
            cgParam = []

        return [psParam, tvParam, psSeriesParam, cgParam]