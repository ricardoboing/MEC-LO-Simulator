from simulator.Simulation import *

def _get_free_time(request):
	service = request.get_service()
	serviceMaxProcessTime = service.get_max_process_time()

	realTime = Simulation.get_clock_pointer()

	return realTime + serviceMaxProcessTime

class MecNode:
	def __init__(self, name, computingPower):
		self.name = name
		self.computingPower = computingPower
		self.freeCpuTime = 0

		self.reset()

	def set_a_new_request_queue(self, QueueClass):
		self.requestQueue = QueueClass()
		print(QueueClass.__name__)

	def receive_request(self, request, force):
		freeCpuTime = self._get_free_cpu_time()
		return self.requestQueue.push_request(request, freeCpuTime, force)

	def get_name(self):
		return self.name

	def get_computing_power(self):
		return self.computingPower

	def has_next_request(self):
		return not self.requestQueue.is_empty()

	def get_current_request_in_process(self):
		return self.currentRequestInProcess

	def finish_current_request_in_process(self):
		assert self.is_busy() == True

		self.isBusy = False
		return self.currentRequestInProcess

	def start_next_request_processing(self):
		assert self.is_busy() == False
		
		if self.has_next_request():
			self.currentRequestInProcess = self.requestQueue.get_first_request()
			self.isBusy = True
			self.freeCpuTime = _get_free_time(self.currentRequestInProcess)

			return True
		else:
			self.freeCpuTime = -1

		return False

	def _get_free_cpu_time(self):
		realTime = Simulation.get_clock_pointer()
		return max(self.freeCpuTime, realTime)

	def is_busy(self):
		return self.isBusy

	def reset(self):
		self.isBusy = False
		self.requestQueue = None
		self.currentRequestInProcess = None