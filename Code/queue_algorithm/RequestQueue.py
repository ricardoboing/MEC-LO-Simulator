class RequestQueue:
	def __init__(self):
		pass

	def push_request(self, request):
		raise Exception("The 'push_request' method is not implemented in the QueueAlgorithm subclass.")

	def get_first_request(self):
		raise Exception("The 'get_first_request' method is not implemented in the QueueAlgorithm subclass.")

	def remove_request(self, request):
		raise Exception("The 'remove_request' method is not implemented in the QueueAlgorithm subclass.")

	def is_empty(self):
		raise Exception("The 'is_empty' method is not implemented in the QueueAlgorithm subclass.")