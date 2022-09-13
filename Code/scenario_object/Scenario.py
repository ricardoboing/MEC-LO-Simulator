from file.InputScenarioReader import *

from scenario_object.MecNode import *
from scenario_object.Service import *

def _create_service_object_list(serviceDict):
	serviceObjectDict = {}
	
	for serviceName in serviceDict:
		deadline = serviceDict[serviceName]["deadline"]
		maxProcessTime = serviceDict[serviceName]["maxProcessTime"]

		serviceObjectDict[serviceName] = Service(deadline, maxProcessTime)

	return serviceObjectDict

def _create_mec_object_list(mecDict):
	mecObjectDict = {}
	
	for mecName in mecDict:
		computerPower = mecDict[mecName]["computerPower"]
		mecObjectDict[mecName] = MecNode(computerPower)

	return mecObjectDict

def _create_request_object_list(requestList, mecObjectDict, serviceObjectDict, intervalForSendingRequests):
	# return [Request(), Request(), ...]
	return None

class Scenario:
	def __init__(self, fileName):
		scenarioReader = InputScenarioReader(fileName)
		
		mecDict = scenarioReader.get_mec_dict()
		serviceDict = scenarioReader.get_service_dict()
		self._requestList = scenarioReader.get_request_dict()

		self._mecObjectDict = _create_mec_object_list(mecDict)
		self._serviceObjectDict = _create_service_object_list(serviceDict)
		self._intervalForSendingRequests = scenarioReader.get_interval_for_sending_requests()

		self.generate_new_request_object_list()

	def generate_new_request_object_list(self):
		self.requestObjectList = _create_request_object_list(
			self._requestList, self._mecObjectDict, self._serviceObjectDict, self._intervalForSendingRequests
		)

	def get_request_object_list(self):
		return self.requestObjectList