from file.output_scenario_writer.Sheet import *

class ComparationSheet(Sheet):
	def __init__(self, sheet):
		super().__init__(sheet)

	def set_distributor_counter(self, counter):
		WorkbookTableWriter.set_cell_value(self.sheet, self.rowIndex, self.columnIndex-1, counter)