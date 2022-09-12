class Request:
	_RequestId = 0
	def __init__(self, user, mec, service, generatedTime, requestId=Request._get_new_id()):
		self.requestId = requestId
		self.user = user
		self.firstMecDestination = mec
		self.generatedTime = generatedTime
		self.responsedTime = -1
		self.service = service

	@staticmethod
	def _get_new_id():
		requestId = Request._RequestId;
		Request._RequestId += 1

		return requestId;

	def set_responsed(self):
		self.responsedTime = Simulator.clockPointer;

	def get_id(self):
		return self.id;

	def get_service(self):
		return self.service;

	def get_first_mec_destination(self):
		return self.firstMecDestination;

	def get_responsed_time(self):
		return self.responsedTime;

	def get_a_clone(self):
		clone = Request(self.user, self.firstMecDestination, self.service, self.generatedTime)