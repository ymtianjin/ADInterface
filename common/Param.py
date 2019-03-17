# encoding=utf-8
import xlrd

class Param:
	testCase = None
	excel = None
	sheet = None

	def __init__(self, testCase, path = None, sheet = None):
		self.testCase = testCase

		if not path is None:
			self.excel = xlrd.open_workbook(path)

		if not path is None and not sheet is None:
			self.sheet = self.excel.sheet_by_name(sheet)

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


#转换得到的值，如果是数组就转换成数组，否则直接返回
	def transValue(self, value):
		if isinstance(value, str)  and len(value) > 2 and value[0] == '[' and value[len(value) -1] == ']':
			value = value.lstrip('[')
			value = value.rstrip(']')
			value = value.split(',')

			return value

		return value


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
		if method == None or url == None:
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
