from file.WorkbookTableReader import *

_MEC_SHEET_NAME = "mec"
_SERVICE_SHEET_NAME = "service"
_REQUEST_SHEET_NAME = "request"
_INTERVAL_FOR_SENDING_REQUESTS_SHEET_NAME = "intervalForSendingRequests"

class InputScenarioReader:
	def __init__(self, fileName):
		self.workbookTable = WorkbookTableReader(fileName)

	def get_mec_dict(self):
		self.workbookTable.set_current_sheet(_MEC_SHEET_NAME)
		return self.workbookTable.get_row_dict_list()

	def get_service_dict(self):
		self.workbookTable.set_current_sheet(_SERVICE_SHEET_NAME)
		return self.workbookTable.get_row_dict_list()

	def get_request_dict(self):
		self.workbookTable.set_current_sheet(_REQUEST_SHEET_NAME)
		return self.workbookTable.get_row_dict_list()

	def get_interval_for_sending_requests(self):
		self.workbookTable.set_current_sheet(_INTERVAL_FOR_SENDING_REQUESTS_SHEET_NAME)
		return self.workbookTable.get_cell_value(0, 1)