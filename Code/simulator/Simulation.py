from simulator.EventScheduler import *
from simulator.SimulatorEvent import *
from simulator.RequestPackage import *

from scenario_object.User import *

class Simulation:
	CurrentSimulation = None
	def __init__(self, DistributorAlgorithmType):
		self.DistributorAlgorithmType = DistributorAlgorithmType
		self.eventScheduler = EventScheduler()
		self.clockPointer = 0
		self.networkTraffic = 0

	def start(self):
		while not self.eventScheduler.is_empty():
			event = self.eventScheduler.get_next_event()
			temporalMoment = event.get_temporal_moment()
			
			self._set_clock_pointer(temporalMoment)
			event.happen()

	def generate_initial_user_event_list(self, requestList):
		for request in requestList:
			package = RequestPackage(request)
			event = SimulatorEvent(User.send_request_package, package)
			self.eventScheduler.push_event(event)

	def get_clock_pointer(self):
		return self.clockPointer

	def get_network_traffic(self):
		return self.networkTraffic

	def increment_network_traffic(self, increment):
		self.networkTraffic += increment
	
	def _set_clock_pointer(self, newPointer):
		if newPointer < self.clockPointer:
			raise Exception("newPointer < self.clockPointer in Simulation class.")

		self.clockPointer = newPointer