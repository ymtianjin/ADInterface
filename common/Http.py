# encoding=utf-8
import unittest, requests, json, logging

class Http:
	testCase = None

	# 构造函数，在类的创建过程中通过编译器调用的函数
	# self指向自己，在实例化对象调用的时候会自动传入，不需要显式调用
	def __init__(self, testCase):
		self.testCase = testCase
		

	# 判断是否是一个下标
	def isIndex(self, key):
		if len(key) > 2 and key[0] == '[' and key[len(key) - 1] == ']':
			key = key.lstrip('[')
			key = key.rstrip(']')
			if key.isdigit():
				return int(key)

		return -1


	def checkResult(self, result, key, value):
		# 校验返回值是否正确，返回键按照/分解成数组，逐层去返回值中查询键值是否正确
		keys = key.split("/")
		keyTip = ""
		curRet = result
		for k in keys:
			if keyTip == "":
				keyTip = k
			else:
				keyTip = keyTip + "/" + k
			# 判断当前节点的键是否是数组下标
			keyIndex = self.isIndex(k)
			if keyIndex > -1:
				if len(curRet) > keyIndex:
					curRet = curRet[keyIndex] # 得到数组的值
				else:
					logging.error("out of range: " + keyTip)

					return False
			elif not curRet.__contains__(k): # 判断键值是否存在
				logging.error("key is not exist: " + keyTip)

				return False
			else:
				curRet = curRet[k] #得到返回的值

		if not value is None:
			if not value == curRet: #判断值是否匹配
				logging.error(keyTip + " value is not match: " + str(value) + " != " + str(curRet))

				return False

		return True



	def checkResponse(self, res, checkResult = None):
		if not res.status_code == 200:
			logging.error("status_code is not 200: " + str(res.status_code))

			return
		if res.text is None or res.text == "":
			logging.error("response is empty")

			return

		if checkResult is None or len(checkResult) == 0:
			logging.info("empty check successfully")

			return

		# 判断返回值是否json对象
		result = json.loads(res.text)
		if not isinstance(result, dict):
			logging.error("parse result failed")

			return
		isOk = True
		for key in checkResult:
			if not self.checkResult(result, key, checkResult[key]):
				isOk = False

		if isOk:
			logging.info("all check successfully")


	def get(self, url, params = None, checkResult = None):
		try:
			res = requests.get(url = url, params = params)
		except BaseException:
			res = "access url failed"

			return res

		self.checkResponse(res, checkResult)

		return res.text


	def  post(self, url, data = None, checkResult = None):
		try:
			res = requests.post(url = url, data = data)
		except BaseException:
			res = "access url failed"

			return res

		self.checkResponse(res, checkResult)

		return res.text