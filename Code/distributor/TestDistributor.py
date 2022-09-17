from distributor.Distributor import *

class TestDistributor(Distributor):
	_QueueType = None#FifoQueue

	@staticmethod
	def send_forward_request(packageRequest):
		#print("TestDistributor.send_forward_request", packageRequest.get_request().get_id())
		return Distributor.send_forward_request(packageRequest)

	@staticmethod
	def send_user_response_request(packageRequest):
		#print("TestDistributor.send_user_response_request", packageRequest.get_request().get_id())
		return Distributor.send_user_response_request(packageRequest)

	@staticmethod
	def receive_user_request(packageRequest):
		#print("TestDistributor.receive_user_request", packageRequest.get_request().get_id())
		return Distributor.receive_user_request(TestDistributor, packageRequest)

	@staticmethod
	def receive_forward_request(packageRequest):
		#print("TestDistributor.receive_forward_request", packageRequest.get_request().get_id())
		return Distributor.receive_forward_request(TestDistributor, packageRequest)
