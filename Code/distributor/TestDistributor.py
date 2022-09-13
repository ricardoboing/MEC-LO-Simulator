from distributor.LoadDistributor import *

class TestDistributor(LoadDistributor):
	QueueType = None#FifoQueue

	@staticmethod
	def send_forward_request(packageRequest):
		print("TestDistributor.send_forward_request", forwardRequest.get_request().get_id())

	@staticmethod
	def send_user_response_request(packageRequest):
		print("TestDistributor.send_user_response_request", forwardRequest.get_request().get_id())

	@staticmethod
	def receive_user_request(packageRequest):
		print("TestDistributor.receive_user_request", forwardRequest.get_request().get_id())

	@staticmethod
	def receive_forward_request(packageRequest):
		print("TestDistributor.receive_forward_request", forwardRequest.get_request().get_id())
