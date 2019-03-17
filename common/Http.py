# encoding=utf-8
import unittest, requests, json, logging

class Http:
	testCase = None
	success = False
	msg = ""

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
					self.msg = "out of range: " + keyTip

					return False
			elif not curRet.__contains__(k): # 判断键值是否存在
				self.msg = "key is not exist: " + keyTip

				return False
			else:
				curRet = curRet[k] #得到返回的值

		if not value is None:
			if not value == curRet: #判断值是否匹配
				self.msg = keyTip + " value is not match: " + str(value) + " != " + str(curRet)

				return False

		return True



	def checkResponse(self, res, checkResult = None):
		if not res.status_code == 200:
			self.msg = "status_code is not 200: " + str(res.status_code)

			return

		if checkResult is None or len(checkResult) == 0:
			self.msg = "empty check successfully"

			return True


		if res.text is None or res.text == "":
			self.msg = "response is empty"

			return False

		#logging.info(res.text)
		# 判断返回值是否json对象
		result = json.loads(res.text)
		if not isinstance(result, dict):
			self.msg = "parse result failed"

			return False
		isOk = True
		for key in checkResult:
			if not self.checkResult(result, key, checkResult[key]):
				isOk = False

		return isOk

	def init(self):
		success = False
		msg = ""

	def finish(self, url, params, res, checkResult):
		if res is None or res.text is None:
			strData = "empty"
		else:
			strData = str(res.text)
		if len(self.msg) > 0:
			self.msg = self.msg + ", data: " + strData + ", except: " + str(checkResult);
		else:
			self.msg = "data: " + strData + ", except: " + str(checkResult);
		logging.info(url + ", result: " + str(self.success) + ", " + self.msg)

	def get(self, url, params = None, checkResult = None):
		self.init()
		try:
			res = requests.get(url = url, params = params)
			self.success = self.checkResponse(res, checkResult)
		except BaseException:
			self.msg = "access url failed"
		self.finish(url, params, res, checkResult)
		

		return self.success


	def  post(self, url, data = None, checkResult = None):
		self.init()
		try:
			res = requests.post(url = url, data = data)
			self.success = self.checkResponse(res, checkResult)
		except BaseException:
			self.msg = "access url failed"
		self.finish(url, params, res, checkResult)

		return self.success