from file.WorkbookTableWriter import *

class Sheet:
	def __init__(self, sheet):
		self.sheet = sheet
		self.rowIndex = 1
		self.columnIndex = 0
		self.columnIndexSet = {}

		self.create_column("time")

	def create_column(self, columnName):
		WorkbookTableWriter.set_cell_value(self.sheet, 0, self.columnIndex, columnName)
		self.columnIndexSet[columnName] = self.columnIndex
		self.columnIndex += 1

	def increment_row_index(self):
		self.rowIndex += 1

	def zero_row_index(self):
		self.rowIndex = 1

	def set_time(self, time):
		columnIndex = self.columnIndexSet["time"]
		WorkbookTableWriter.set_cell_value(self.sheet, self.rowIndex, columnIndex, time)