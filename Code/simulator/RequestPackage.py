class RequestPackage:
	def __init__(self, request, forwardCounter=0):
		self.forwardCounter = forwardCounter
		self.request = request

	def get_request(self):
		return self.request

	def get_forward_counter(self):
		return self.forwardCounter