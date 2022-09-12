class LoadDistributor:
	QueueType = None

	@staticmethod
	def send_forward_request(forwardRequest):
		raise Exception("The 'send_forward_request' method is not implemented in the DistributorAlgorithm subclass.")

	@staticmethod
	def send_user_response_request(request):
		raise Exception("The 'send_user_response_request' method is not implemented in the DistributorAlgorithm subclass.")

	@staticmethod
	def receive_user_request(request):
		raise Exception("The 'receive_user_request' method is not implemented in the DistributorAlgorithm subclass.")

	@staticmethod
	def receive_forward_request(forwardRequest):
		raise Exception("The 'receive_forward_request' method is not implemented in the DistributorAlgorithm subclass.")
