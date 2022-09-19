from queue_algorithm.preferential_queue.Block import *

class RequestBlock(Block):
	def __init__(self, start, end, request):
		super().__init__(start, end)
		self.request = request

	def get_request(self):
		return self.request