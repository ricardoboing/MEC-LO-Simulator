from file.output_scenario_writer.Sheet import *

class DistributorSheet(Sheet):
	def __init__(self, distributorName, sheet):
		super().__init__(sheet)
		self.distributorName = distributorName

		self.create_column("success_counter")
		self.create_column("fail_counter")
		self.create_column("network")

	def get_distributor_name(self):
		return self.distributorName

	def set_network(self, network):
		columnIndex = self.columnIndexSet["network"]
		WorkbookTableWriter.set_cell_value(self.sheet, self.rowIndex, columnIndex, network)

	def set_success_counter(self, successCounter):
		columnIndex = self.columnIndexSet["success_counter"]
		WorkbookTableWriter.set_cell_value(self.sheet, self.rowIndex, columnIndex, successCounter)

	def set_fail_counter(self, failCounter):
		columnIndex = self.columnIndexSet["fail_counter"]
		WorkbookTableWriter.set_cell_value(self.sheet, self.rowIndex, columnIndex, failCounter)