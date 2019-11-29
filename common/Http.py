# encoding=utf-8
__author__ = 'limeng'
import unittest, requests, json, logging, time, os
from common import Parser, Navigate, DeviceLog

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

	def assignValue(self, key):
		if not isinstance(key, str) or len(key) < 10:
			return key

		prev = 0
		while True:
			begin = key.find("{$global_", prev)
			if begin < 0:
				break
			begin += 2
			end = key.find("}", begin)
			if end < 0:
				break
			name = key[begin:end]
			prev = end + 1
			if not self.variable.__contains__(name):
				continue
			value = self.variable[name]
			if isinstance(value, list) and len(key) > (end + 3) and key[end + 1] == '[':
				begin = end + 2
				end = key.find(']', begin)
				index = -1
				if end > begin:
					index = key[begin:end]
				if index.isdigit() and 0 <= int(index) < len(value):
					name = "{$" + name + "}[" + index + "]"
					key = key.replace(name, value[int(index)])
			else:
				name = "{$" + name + "}"
				key = key.replace(name, str(value))

		return key

	def evalValue(self, value):
		if not isinstance(value, str):
			return value
		try:
			test = json.loads(value)
			if not isinstance(test, dict):
				return value
			return test
		except BaseException:
			return value

	def assignData(self, data):
		if data is None or len(data) == 0:
			return
		for key in data:
			value = self.assignValue(data[key])
			data[key] = self.evalValue(value)

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
					curRet = None
					break
			elif not curRet.__contains__(v): # 判断键值是否存在
				curRet = None
				break
			else:
				curRet = curRet[v] #得到返回的值

		self.variable[name] = curRet

		return (curRet is None)



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

	def readValue(self, res, variable = None):
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

	def init(self, data = None):
		self.success = False
		self.msg = ""
		self.assignData(data)

	def finish(self, url, data, res, checkResult):
		if res is None or res.text is None:
			strData = "empty"
		else:
			strData = str(res.text)
		self.msg = (len(self.msg) > 0 and self.msg + ", " or "") + "data: " + str(data) + ", response: " + strData + ", except: " + str(checkResult);
		logging.info(url + ", result: " + str(self.success) + ", " + self.msg)

	def define_proc(self, params = None, checkResult = None, variable = None):
		for name in params:
			self.variable[name] = self.assignValue(params[name])

	def split_proc(self, params=None, checkResult=None, variable=None):
		for name in params:
			if self.variable.__contains__(name) and isinstance(self.variable[name], str):
				self.variable[name] = self.variable[name].split(params[name])

	def join_proc(self, params=None, checkResult=None, variable=None):
		for name in params:
			if self.variable.__contains__(name) and isinstance(self.variable[name], list):
				self.variable[name] = params[name].join(self.variable[name])

	def substr_proc(self, params=None, checkResult=None, variable=None):
		for name in params:
			if self.variable.__contains__(name) and isinstance(self.variable[name], str):
				seq = params[name].split(":")
				if len(seq) == 2:
					begin = int(seq[0])
					end = int(seq[1])
					length = len(self.variable[name])
					if end > begin and begin < length and end < length:
						self.variable[name] = self.variable[name][begin:end]

	def click_proc(self, params=None, checkResult=None, variable=None):
		self.init()
		if not isinstance(params, dict):
			params = {}
		self.assignData(params)
		if not isinstance(checkResult, dict):
			params = {}
		self.assignData(checkResult)

		# 获取cms的推荐位
		parser = Parser.Parser()
		parser.appChannel("8acb5c18e56c1988723297b1a8dc9260", "600001")
		clickParams = parser.filter(params)

		# 目前其实还只支持点击一个，因为第一次跑完后appuim就退出了，并且测试用例的结果也只支持一次，后面会覆盖前面的结果
		# 后续改进是把每次点击都触发一个测试用例，并且单独记录结果集，并且可以自动启动appium
		navigate = Navigate.Naviage()
		for param in clickParams:
			if len(param) < 1:
				continue
			logging.info("click ad space: " + str(param))
			# 通过adb记录设备日志
			logPath = os.path.join(os.getcwd(), 'results/device_logs/')
			logFile = os.path.join(logPath, time.strftime('%Y%m%d%H%M%S') + 'DeviceLog.log')
			if not os.path.exists(logPath):
				os.makedirs(logPath)
			deviceLog = DeviceLog.DeviceLog()
			deviceLog.connect("192.168.22.34", "14499M580068257")
			deviceLog.clear_cache("com.newtv.cboxtv")
			deviceLog.log_start(logFile)

			# 通过appium启动遍历
			if navigate.startup():
				navigate.click(param)
				deviceLog.disconnect()
			else:
				self.success = False
				self.msg = "device can't be connected"
				deviceLog.disconnect()
				continue

			missionMid = deviceLog.log_read(logFile, checkResult)
			if len(missionMid) > 0:
				self.success = False
				strSplit = ","
				self.msg = "mid: " + strSplit.join(missionMid) + " can't be found"
			else:
				self.success = True

		navigate.disconnect()

	def function(self, url, params = None, checkResult = None, variable = None):
		if url == "define" and params is not None:
			self.define_proc(params, checkResult, variable)
		elif url == "split" and params is not None:
			self.split_proc(params, checkResult, variable)
		elif url == "join" and params is not None:
			self.join_proc(params, checkResult, variable)
		elif url == "substr" and params is not None:
			self.substr_proc(params, checkResult, variable)
		elif url == "click":
			self.click_proc(params, checkResult, variable)


	def get(self, url, params = None, checkResult = None, variable = None):
		url = self.assignValue(url)
		self.init(params)
		res = None
		try:
			res = requests.get(url = url, params = params)
			self.success = self.checkResponse(res, checkResult)
			self.readValue(res, variable)
		except BaseException:
			self.msg = "access url failed"
		self.finish(url, params, res, checkResult)
		

		return self.success


	def  post(self, url, data = None, checkResult = None, variable = None):
		url = self.assignValue(url)
		self.init(data)
		res = None
		try:
			headers = {'Content-Type': 'application/json'}
			res = requests.post(url = url, data = json.dumps(data), headers = headers)
			self.success = self.checkResponse(res, checkResult)
			self.readValue(res, variable)
		except BaseException:
			self.msg = "access url failed"
		self.finish(url, data, res, checkResult)

		return self.success