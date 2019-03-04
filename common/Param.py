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


	def turn(self, sheet):
		self.sheet = self.excel.sheet_by_name(sheet)


	def read(self, row, col):
		try:
			ctype = self.sheet.cell(row, col).ctype
			if ctype == 0 or ctype == 5:
				return None
			if ctype == 2:
				return int(self.sheet.cell(row, col).value)
			return self.sheet.cell(row, col).value
		except BaseException:
			return None


	def transValue(self, value):
		if (isinstance(value, str) or isinstance(value, unicode)) and len(value) > 2 and value[0] == '[' and value[len(value) -1] == ']':
			value = value.lstrip('[')
			value = value.rstrip(']')
			value = value.split(',')

			return value

		return value


	def caseCount(self):
		return len(self.excel.sheet_names())


	def switchCase(self, caseIndex):
		self.sheet = self.excel.sheet_by_index(caseIndex)

		return self.sheet.name;


	def readStep(self, startFrom = 1):
		method = self.read(startFrom, 0)
		url = self.read(startFrom, 1)
		count = self.read(startFrom, 6)
		if method == None or url == None:
			return None
		if count == None:
			count = 1
		if isinstance(count, str) and not count.isdigit():
			count = 1
		address = {'method': method, 'url': url, 'count': int(count)}

		return address


	def readData(self, startFrom = 1):
		row = startFrom
		data = {}
		while True:
			name = self.read(row, 2)
			if name is None or name == "":
				break
			value = self.read(row, 3)
			data[name] = self.transValue(value)
			row += 1

		return data;


	def readCheck(self, startFrom = 1):
		row = startFrom
		check = {}
		while True:
			name = self.read(row, 4)
			if name is None or name == "":
				break
			value = self.read(row, 5)
			if value == "":
				check[name] = None
			else:
				check[name] = value
			row += 1

		return check;
