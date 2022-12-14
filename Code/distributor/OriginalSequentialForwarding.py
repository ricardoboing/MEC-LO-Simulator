from distributor.Distributor import *
from queue_algorithm.Fifo import *

class OriginalSequentialForwarding:
	QueueClass = Fifo
	FORWARD_LIMIT = 2

	def receive_forward_request(packageRequest):
		return OriginalSequentialForwarding.receive_user_request(packageRequest)

	@staticmethod
	def receive_user_request(packageRequest):
		request = packageRequest.get_request()
		mec = packageRequest.get_destination()

		forwardCount = packageRequest.get_forward_counter()
		forceLocalProcessing = forwardCount >= OriginalSequentialForwarding.FORWARD_LIMIT

		succes = mec.receive_request(request, forceLocalProcessing)

		if succes:
			mecIsBusy = mec.is_busy()

			if not mecIsBusy:
				return Distributor.start_next_request_processing(mec)
		else:
			return Distributor.send_forward_request(packageRequest)
			
		return None