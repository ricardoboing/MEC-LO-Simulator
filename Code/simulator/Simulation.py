class Simulation:
	CurrentSimulation = None
	def __init__(self, DistributorAlgorithmType):
		self.DistributorAlgorithmType = DistributorAlgorithmType
		self.eventScheduler = EventScheduler()
		self.clockPointer = 0
		self.networkTraffic = 0

	def start_simulation(self, requestList):
		pass

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