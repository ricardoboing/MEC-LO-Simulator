from LoadDistributor import *

class TestDistributor(LoadDistributor):
	QueueType = None#FifoQueue

	@staticmethod
	def send_forward_request(forwardRequest):
		print("TestDistributor.send_forward_request")

	@staticmethod
	def send_user_response_request(request):
		print("TestDistributor.send_user_response_request")

	@staticmethod
	def receive_user_request(request):
		print("TestDistributor.receive_user_request")

	@staticmethod
	def receive_forward_request(forwardRequest):
		print("TestDistributor.receive_forward_request")
