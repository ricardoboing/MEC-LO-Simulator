from file.WorkbookTableFile import *

_MEC_SHEET_NAME = "mec"
_SERVICE_SHEET_NAME = "service"
_REQUEST_SHEET_NAME = "request"
_INTERVAL_FOR_SENDING_REQUESTS_SHEET_NAME = "intervalForSendingRequests"

class InputScenarioReader:
	def __init__(self, fileName):
		self.workbookTable = WorkbookTableFile(fileName)

	def get_mec_dict(self):
		self.workbookTable.set_current_sheet(_MEC_SHEET_NAME)
		mecDict = {}

		rowIndex = 1
		while True:
			mecName = self.workbookTable.get_row_name(rowIndex)
			computerPower = self.workbookTable.get_cell_value(rowIndex, 1)

			if mecName == None:
				break

			mecDict[mecName] = {
				"computerPower": computerPower
			}

			rowIndex += 1

		return mecDict

	def get_service_dict(self):
		self.workbookTable.set_current_sheet(_SERVICE_SHEET_NAME)
		serviceDict = {}

		rowIndex = 1
		while True:
			serviceName = self.workbookTable.get_row_name(rowIndex)
			maxProcessTime = self.workbookTable.get_cell_value(rowIndex, 1)
			deadline = self.workbookTable.get_cell_value(rowIndex, 2)

			if serviceName == None:
				break

			serviceDict[serviceName] = {
				"maxProcessTime": maxProcessTime,
				"deadline": deadline
			}

			rowIndex += 1

		return serviceDict

	def get_request_dict(self):
		self.workbookTable.set_current_sheet(_REQUEST_SHEET_NAME)
		
		requestDict = {}
		rowIndex = 1
		
		while True:
			mecName = self.workbookTable.get_row_name(rowIndex)
			if mecName == None:
				break

			requestDict[mecName] = {}
			columnIndex = 1

			while True:
				serviceName = self.workbookTable.get_column_name(columnIndex)
				numberOfRequests = self.workbookTable.get_cell_value(rowIndex, columnIndex)

				if serviceName == None:
					break

				requestDict[mecName][serviceName] = numberOfRequests

				columnIndex += 1
			rowIndex += 1

		return requestDict


	def get_interval_for_sending_requests(self):
		self.workbookTable.set_current_sheet(_INTERVAL_FOR_SENDING_REQUESTS_SHEET_NAME)
		return self.workbookTable.get_cell_value(0, 1)