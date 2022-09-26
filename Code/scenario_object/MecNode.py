class MecNode:
	def __init__(self, name, computingPower):
		self.name = name
		self.computingPower = computingPower

		self.reset()

	def set_a_new_request_queue(self, QueueClass):
		self.requestQueue = QueueClass()

	def receive_request(self, request, force=False): # force when forwarded > limit (some algorithms)
		return self.requestQueue.push_request(request)

# forwardRequest = RequestPackage(request)

	def get_name(self):
		return self.name

	def get_computing_power(self):
		return self.computingPower

	def has_next_request(self):
		return not self.requestQueue.is_empty()

	def get_current_request_in_process(self):
		return self.currentRequestInProcess

	def finish_current_request_in_process(self):
		self.isBusy = False
		return self.currentRequestInProcess

	def set_next_current_request_in_process(self):
		assert self.is_busy() == False
		
		if self.has_next_request():
			self.currentRequestInProcess = self.requestQueue.get_first_request()
			self.isBusy = True

			return True
		return False

	def is_busy(self):
		return self.isBusy

	def reset(self):
		self.isBusy = False
		self.requestQueue = None
		self.currentRequestInProcess = None