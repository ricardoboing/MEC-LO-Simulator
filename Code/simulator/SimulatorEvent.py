class SimulatorEvent:
	def __init__(self, function, parameters, temporalMoment):
		self.function = function
		self.parameters = parameters
		self.temporalMoment = temporalMoment

	def happen(self):
		return self.function( self.parameters )

	def get_temporal_moment(self):
		return self.temporalMoment

	@staticmethod
	def generate_new_event(eventFunction, parameters, delay):
		from simulator.Simulation import Simulation

		realTime = Simulation.get_clock_pointer()
		temporalMoment = realTime + delay

		return SimulatorEvent(eventFunction, parameters, temporalMoment)