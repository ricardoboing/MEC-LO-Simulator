class SimulatorEvent:
	def __init__(self, function, requestPackage, temporalMoment):
		self.function = function
		self.requestPackage = requestPackage
		self.temporalMoment = temporalMoment

	def happen(self):
		return self.function( self.requestPackage )

	def get_temporal_moment(self):
		return self.temporalMoment

	@staticmethod
	def generate_new_event(eventFunction, requestPackage, delay):
		from simulator.Simulation import Simulation

		realTime = Simulation.get_clock_pointer()
		temporalMoment = realTime + delay

		return SimulatorEvent(eventFunction, requestPackage, temporalMoment)