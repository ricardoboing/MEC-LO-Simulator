from file.WorkbookTableWriter import *

from file.output_scenario_writer.DistributorSheet import *
from file.output_scenario_writer.ComparationSheet import *

_SUCCESS_SHEET_NAME = "success"
_FAIL_SHEET_NAME = "fail"
_NETWORK_SHEET_NAME = "network"
_FORWARD_SHEET_NAME = "forward"

class OutputScenarioWriter:
	def __init__(self, fileName):
		self.workbookTable = WorkbookTableWriter(fileName)
		self.distributorCounter = 0

		successSheet = self.workbookTable.create_sheet(_SUCCESS_SHEET_NAME)
		failSheet = self.workbookTable.create_sheet(_FAIL_SHEET_NAME)
		networkSheet = self.workbookTable.create_sheet(_NETWORK_SHEET_NAME)
		forwardSheet = self.workbookTable.create_sheet(_FORWARD_SHEET_NAME)

		self.successSheet = ComparationSheet(successSheet)
		self.failSheet = ComparationSheet(failSheet)
		self.networkSheet = ComparationSheet(networkSheet)
		self.forwardSheet = ComparationSheet(forwardSheet)

		self.distributorSheetList = []

	def create_distributor_sheet(self, distributorName):
		numberOfDistributors = len(self.distributorSheetList)
		distributorName = str(numberOfDistributors) + distributorName
		
		newDistributorSheet = self.workbookTable.create_sheet(distributorName)
		self.distributorSheetList.append(
			DistributorSheet(distributorName, newDistributorSheet)
		)

		self.successSheet.zero_row_index()
		self.successSheet.create_column(distributorName)
		
		self.failSheet.zero_row_index()
		self.failSheet.create_column(distributorName)
		
		self.networkSheet.zero_row_index()
		self.networkSheet.create_column(distributorName)

		self.forwardSheet.zero_row_index()
		self.forwardSheet.create_column(distributorName)

	def increment_row_index(self):
		currentDistributorSheet = self.distributorSheetList[-1]

		self.successSheet.increment_row_index()
		self.failSheet.increment_row_index()
		self.networkSheet.increment_row_index()
		self.forwardSheet.increment_row_index()
		currentDistributorSheet.increment_row_index()

	def set_row_in_distributor_sheet(self, time, success, fail, network, forwardCounter):
		currentDistributorSheet = self.distributorSheetList[-1]

		currentDistributorSheet.set_time(time)
		currentDistributorSheet.set_network(network)
		currentDistributorSheet.set_success_counter(success)
		currentDistributorSheet.set_fail_counter(fail)
		currentDistributorSheet.set_forward_counter(forwardCounter)

	def set_row_in_success_sheet(self, time, success):
		self.successSheet.set_time(time)
		self.successSheet.set_distributor_counter(success)

	def set_row_in_fail_sheet(self, time, fail):
		self.failSheet.set_time(time)
		self.failSheet.set_distributor_counter(fail)

	def set_row_in_network_sheet(self, time, network):
		self.networkSheet.set_time(time)
		self.networkSheet.set_distributor_counter(network)

	def set_row_in_forward_sheet(self, time, forwardCounter):
		self.forwardSheet.set_time(time)
		self.forwardSheet.set_distributor_counter(forwardCounter)

	def save(self):
		self.workbookTable.save()