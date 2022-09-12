from file.WorkbookTableFile import *

class InputScenarioReader:
	def __init__(self, fileName):
		self.workbookTable = WorkbookTableFile(fileName)

	def get_mec_list(self):
		self.workbookTable.set_current_sheet("mec")
		mecSet = {}

		rowIndex = 1
		while True:
			mecName = self.workbookTable.get_row_name(rowIndex)
			computerPower = self.workbookTable.get_cell_value(rowIndex, 1)

			if mecName == None:
				break

			mecSet[mecName] = {
				"computerPower": computerPower
			}

			rowIndex += 1

		return mecSet

	def get_service_list(self):
		self.workbookTable.set_current_sheet("service")
		serviceSet = {}

		rowIndex = 1
		while True:
			serviceName = self.workbookTable.get_row_name(rowIndex)
			processTime = self.workbookTable.get_cell_value(rowIndex, 1)
			deadline = self.workbookTable.get_cell_value(rowIndex, 2)

			if serviceName == None:
				break

			serviceSet[serviceName] = {
				"processTime": processTime,
				"deadline": deadline
			}

			rowIndex += 1

		return serviceSet

	def get_request_list(self):
		self.workbookTable.set_current_sheet("request")
		
		requestSet = {}
		rowIndex = 1
		
		while True:
			mecName = self.workbookTable.get_row_name(rowIndex)
			if mecName == None:
				break

			requestSet[mecName] = {}
			columnIndex = 1

			while True:
				serviceName = self.workbookTable.get_column_name(columnIndex)
				numberOfRequests = self.workbookTable.get_cell_value(rowIndex, columnIndex)

				if serviceName == None:
					break

				requestSet[mecName][serviceName] = numberOfRequests

				columnIndex += 1
			rowIndex += 1

		return requestSet


	def get_interval_for_sending_requests(self):
		simulationSheet = self.file["simulation"]