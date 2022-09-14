import random

from file.InputScenarioReader import *

from scenario_object.MecNode import *
from scenario_object.Service import *
from scenario_object.Request import *
from scenario_object.User import *

def _create_service_object_dict(serviceDict):
	serviceObjectDict = {}
	
	for serviceName in serviceDict:
		deadline = serviceDict[serviceName]["deadline"]
		maxProcessTime = serviceDict[serviceName]["maxProcessTime"]

		serviceObjectDict[serviceName] = Service(serviceName, deadline, maxProcessTime)

	return serviceObjectDict

def _create_mec_object_list(mecDict):
	mecObjectDict = {}
	mecList = []
	
	for mecName in mecDict:
		computerPower = mecDict[mecName]["computerPower"]
		mecNode = MecNode(mecName, computerPower)
		
		mecObjectDict[mecName] = mecNode
		mecList.append(mecNode)

	return mecList, mecObjectDict

def _create_random_request_object(userObject, mecObject, serviceObject, intervalForSendingRequests):
	generatedTime = random.randint(0, intervalForSendingRequests)
	return Request(userObject, mecObject, serviceObject, generatedTime)

def _create_request_object_list(requestDict, mecObjectDict, serviceObjectDict, intervalForSendingRequests):
	userObject = User()
	#requestListPerService = {}
	requestList = []

	for mecName in requestDict:
		mecDict = requestDict[mecName]
		mecObject = mecObjectDict[mecName]

		for serviceName in mecDict:
			serviceObject = serviceObjectDict[serviceName]
			numberOfRequests = mecDict[serviceName]

			#if serviceName not in requestListPerService:
			#	requestListPerService[serviceName] = []

			for i in range(0, numberOfRequests):
				requestObject = _create_random_request_object(
					userObject, mecObject, serviceObject, intervalForSendingRequests
				)

				requestList.append(requestObject)
				#requestListPerService[serviceName].append(requestObject)
	
	return requestList

class Scenario:
	def __init__(self, fileName):
		scenarioReader = InputScenarioReader(fileName)
		
		mecDict = scenarioReader.get_mec_dict()
		serviceDict = scenarioReader.get_service_dict()
		self._requestDict = scenarioReader.get_request_dict()

		self._mecList, self._mecObjectDict = _create_mec_object_list(mecDict)
		self._serviceObjectDict = _create_service_object_dict(serviceDict)
		self._intervalForSendingRequests = scenarioReader.get_interval_for_sending_requests()

		self.generate_new_request_object_list()

	def generate_new_request_object_list(self):
		self.requestObjectList = _create_request_object_list(
			self._requestDict, self._mecObjectDict, self._serviceObjectDict, self._intervalForSendingRequests
		)

	def get_request_object_list(self):
		return self.requestObjectList

	def get_mec_list(self):
		return self._mecList