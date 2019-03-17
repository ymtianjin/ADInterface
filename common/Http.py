# encoding=utf-8
import unittest, requests, json, logging

class Http:

	# 构造函数，在类的创建过程中通过编译器调用的函数
	# self指向自己，在实例化对象调用的时候会自动传入，不需要显式调用
	def __init__(self, testCase):
		self.testCase = testCase
		self.success = False
		self.msg = ""
		self.variable = {}
		

	# 判断是否是一个下标
	def isIndex(self, key):
		if len(key) > 2 and key[0] == '[' and key[len(key) - 1] == ']':
			key = key.lstrip('[')
			key = key.rstrip(']')
			if key.isdigit():
				return int(key)

		return -1

	def isVariableName(self, key):
		if isinstance(key, str) and len(key) > 2 and key[0] == '{' and key[len(key) - 1] == '}' and key.find("{global_") == 0:
			key = key.lstrip('{')
			key = key.rstrip('}')
			if self.variable.__contains__(key):
				return key
		return None


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

	def readResult(self, result, name, value):
		# 校验返回值是否正确，返回键按照/分解成数组，逐层去返回值中查询键值是否正确
		values = value.split("/")
		curRet = result
		for v in values:
			valueIndex = self.isIndex(v)
			if valueIndex > -1:
				if len(curRet) > valueIndex:
					curRet = curRet[valueIndex] # 得到数组的值
				else:
					return None
			elif not curRet.__contains__(v): # 判断键值是否存在
				return None
			else:
				curRet = curRet[v] #得到返回的值

		if not curRet is None:
			self.variable[name] = curRet
			return True

		return False



	def checkResponse(self, res, checkResult = None):
		if not res.status_code == 200:
			self.msg = "status_code is not 200: " + str(res.status_code)

			return False

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

	def readVariable(self, res, variable = None):
		if not res.status_code == 200:
			return False

		if variable is None or len(variable) == 0:
			return True


		if res.text is None or res.text == "":
			return False

		result = json.loads(res.text)
		if not isinstance(result, dict):
			return False

		for key in variable:
			self.readResult(result, key, variable[key])

		return True

	def init(self, data):
		self.success = False
		self.msg = ""
		print(str(data))
		if not data is None and len(data) > 0:
			for key in data:
				name = self.isVariableName(data[key])
				if not name is None:
					data[key] = self.variable[name]
		print(str(data))

	def finish(self, url, res, checkResult):
		if res is None or res.text is None:
			strData = "empty"
		else:
			strData = str(res.text)
		if len(self.msg) > 0:
			self.msg = self.msg + ", data: " + strData + ", except: " + str(checkResult);
		else:
			self.msg = "data: " + strData + ", except: " + str(checkResult);
		logging.info(url + ", result: " + str(self.success) + ", " + self.msg)

	def get(self, url, params = None, checkResult = None, variable = None):
		self.init(params)
		try:
			res = requests.get(url = url, params = params)
			self.success = self.checkResponse(res, checkResult)
			self.readVariable(res, variable)
		except BaseException:
			self.msg = "access url failed"
		self.finish(url, res, checkResult)
		

		return self.success


	def  post(self, url, data = None, checkResult = None, variable = None):
		self.init(data)
		try:
			res = requests.post(url = url, data = data)
			self.success = self.checkResponse(res, checkResult)
			self.readVariable(res, variable)
		except BaseException:
			self.msg = "access url failed"
		self.finish(url, res, checkResult)

		return self.success