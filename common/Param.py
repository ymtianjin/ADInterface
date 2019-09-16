# encoding=utf-8
import xlrd, json

class Param:

	def __init__(self, testCase, path = None, sheet = None):
		self.testCase = testCase

		if not path is None:
			self.excel = xlrd.open_workbook(path)
		else:
			self.excel = None

		if not path is None and not sheet is None:
			self.sheet = self.excel.sheet_by_name(sheet)
		else:
			self.sheet = None

	#打开excel文件
	def reopen(self, path, sheet = None):
		try:
			self.excel = xlrd.open_workbook(path)
			if not sheet is None:
				self.sheet = self.excel.sheet_by_name(sheet)
			else:
				self.sheet = None
		except BaseException:
			return False

		return True

	#切换sheet
	def turn(self, sheet):
		self.sheet = self.excel.sheet_by_name(sheet)

	#读sheet中单元格的数据
	def read(self, row, col):
		try:
			ctype = self.sheet.cell(row, col).ctype  #单元格数据类型
			if ctype == 0 or ctype == 5:  # 0或5 是空
				return None
			if ctype == 2: #整形
				return int(self.sheet.cell(row, col).value)
			return self.sheet.cell(row, col).value
		except BaseException:
			return None


	def isEmpty(self, value):
		if len(value) == 0:
			return True

		for c in value:
			if c == ' ' or c == '\n' or c == '\r' or c == '\t':
				pass
			else:
				return False

		return True


	def isArray(self, value):
		if isinstance(value, str)  and len(value) > 2:
			length = len(value)
			start = value.find('[')
			end = value.rfind(']')
			if start >= 0 and end > start:
				strFront = value[0 : start]
				strTail = value[end + 1 : len(value) - end]
				if self.isEmpty(strFront) and self.isEmpty(strTail):
					return (start, end)

		return (-1, -1)


	def stripArray(self, arr):
		for n in range(0, len(arr)):
			if isinstance(arr[n], str):
				arr[n] = arr[n].strip()

	
	#转换得到的值，如果是数组就转换成数组，否则直接返回
	def transValue(self, value):
		if not isinstance(value, str)  or len(value) < 2:
			return value
			
		data = None
		try:
			data = json.loads(value)	
		except json.JSONDecodeError:
			pass		
		finally:
			if data is not None:
				return data

		start, end = self.isArray(value)
		if start < 0 or end < 0:
			return value

		value = value[start + 1 : end]
		if len(value) > 0:
			start = value.find('[')
			end = value.rfind(']')
			if start >= 0 and end > start:
				arr = []
				str1 = value[0 : start]
				dotIndex = str1.rfind(',')
				if dotIndex >= 0:
					str1 = str1[0 : dotIndex]
				str2 = value[start : end + 1]
				str3 = value[end + 1 : len(value)]
				dotIndex = str3.find(',')
				if dotIndex >= 0:
					str3 = str3[dotIndex + 1 : len(str3)]
				if not self.isEmpty(str1):
					arr.extend(str1.split(','))
				child = self.transValue(str2)
				arr.append(child)
				if not self.isEmpty(str3):
					arr.extend(str3.split(','))
			else:
				arr = value.split(',')
		else:
			arr = []
		self.stripArray(arr)

		return arr


	#获得用例数量
	def caseCount(self):
		return len(self.excel.sheet_names())


	#切换用例
	def switchCase(self, caseIndex):
		self.sheet = self.excel.sheet_by_index(caseIndex)

		return self.sheet.name;

	#读取调用方法、地址、执行次数
	def readStep(self, startFrom = 1):
		name = self.read(startFrom, 0)
		method = self.read(startFrom, 1)
		url = self.read(startFrom, 2)
		if method == None:
			return None
		if name is None:
			name = url
		address = {'name': name, 'method': method, 'url': url}

		return address


	#读取参数
	def readData(self, startFrom = 1):
		row = startFrom #开始读的行
		data = {}
		while True:
			name = self.read(row, 3)
			if name is None or name == "": #没有参数，表示读取结束
				break
			value = self.read(row, 4)
			data[name] = self.transValue(value)
			row += 1

		return data;

	#读期望值
	def readCheck(self, startFrom = 1):
		row = startFrom
		check = {}
		while True:
			name = self.read(row, 5)
			if name is None or name == "":
				break
			value = self.read(row, 6)
			if value == "":
				check[name] = None
			else:
				check[name] = value
			row += 1

		return check;

	#读取全局变量
	#变量包括变量名字和获取变量的字段，变量名必须以"global_"开头
	#变量值在后续的步骤中可以通过"[global_xxxx]"的方式访问
	def readVariable(self, startFrom = 1):
		row = startFrom
		variable = {}
		while True:
			name = self.read(row, 7)
			if name is None or name == "" or name.find("global_") != 0:
				break
			value = self.read(row, 8)
			if value is None or value == "":
				break
			variable[name] = value
			row += 1

		return variable;
