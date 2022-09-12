def _create_service_object_list(serviceList):
	# return {"s1": Service(), "s2": Service(), ...}
	pass

def _create_mec_object_list(mecList):
	# return {"m1": Mec(), "m2": Mec(), ...}
	pass

def _create_request_object_list(requestList, intervalForSendingRequests):
	# return [Request(), Request(), ...]
	pass

class Scenario:
	def __init__(self, serviceList, mecList, requestList, intervalForSendingRequests):
		self.intervalForSendingRequests = intervalForSendingRequests
		
		serviceObjectList = _create_service_object_list(serviceList)
		mecObjectList = _create_mec_object_list(mecList)
		
		self.requestObjectList = _create_request_object_list(requestList, intervalForSendingRequests)

	def get_request_object_list(self):
		# return a clone list for requestObjectList
		pass