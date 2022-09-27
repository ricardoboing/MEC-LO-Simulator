from simulator.Simulation import *

class Request:
	_RequestId = 0
	def __init__(self, user, mec, service, generatedTime, requestId=None):
		if requestId == None:
			self.requestId = Request._get_new_id()
		else:
			self.requestId = requestId
		
		self.user = user
		self.firstMecDestination = mec
		self.generatedTime = generatedTime
		self.responsedTime = -1
		self.service = service

	@staticmethod
	def _get_new_id():
		requestId = Request._RequestId
		Request._RequestId += 1

		return requestId

	def set_responsed(self):
		self.responsedTime = Simulation.get_clock_pointer()

	def get_id(self):
		return self.requestId

	def get_generated_time(self):
		return self.generatedTime

	def get_service(self):
		return self.service

	def get_first_mec_destination(self):
		return self.firstMecDestination

	def get_responsed_time(self):
		return self.responsedTime

	def get_service(self):
		return self.service

	def met_the_deadline(self):
		serviceDeadline = self.service.get_deadline()
#		print(self.generatedTime, serviceDeadline, self.responsedTime, self.generatedTime + serviceDeadline >= self.responsedTime)
		return self.generatedTime + serviceDeadline >= self.responsedTime

	def get_a_clone(self):
		return Request(self.user, self.firstMecDestination, self.service, self.generatedTime, self.requestId)