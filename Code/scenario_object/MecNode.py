class MecNode:
	def __init__(self, computingPower):
		self.isBusy = True
		self.computingPower = computingPower
		self.requestQueue = None
		self.currentRequestInProcess = None

	def set_a_new_request_queue(self, QueueType):
		self.requestQueue = QueueType()

	def receive_request(self, request, force): # force when forwarded > limit (some algorithms)
		success = self.requestQueue.push_request(request)

		if not success:
			forwardRequest = ForwardRequest(request)
			# Forward the request when the request deadline will extrapolated
			# Use the distributor algorithm for forward the request

	def get_computing_power(self):
		return self.computingPower

	def get_next_request(self):
		return self.requestQueue.get_first_request()

	def has_next_request(self):
		return self.requestQueue.is_empty()

	def get_current_request_in_process(self):
		return self.currentRequestInProcess

	def finish_current_request_in_process(self):
		pass

	def set_next_current_request_in_process(self):
		pass

	def reset(self):
		pass