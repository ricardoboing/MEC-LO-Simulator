from queue_algorithm.preferential_queue.Block import *

class RequestBlock(Block):
	def __init__(self, width, end, request):
		super().__init__(width, end)
		self.request = request

	def get_request(self):
		return self.request