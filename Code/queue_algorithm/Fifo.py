from queue_algorithm.RequestQueue import *
from simulator.Simulation import *

class Fifo(RequestQueue):
	def __init__(self):
		self.queue = []

	def push_request(self, request, force):
		if force:
			self.queue.append(request)
			return True
		
		service = request.get_service()
		processTime = service.get_max_process_time()

		end = service.get_deadline()
		end += request.get_generated_time()
		
		start = end - processTime
		realTime = Simulation.get_clock_pointer()

		if realTime > start:
			return False

		load = realTime

		for i in range (0, len(self.queue)):
			_request = self.queue[i]
			_service = _request.get_service()
			_processTime = _service.get_max_process_time()

			load += _processTime

			if load > start:
				return False

		self.queue.append(request)
		return True

	def get_first_request(self):
		return self.queue.pop(0)

	def is_empty(self):
		return len(self.queue) == 0