class SimulatorEvent:
	def __init__(self, temporalMoment, function, request):
		self.temporalMoment = temporalMoment
		self.function = function
		self.request = request

	def get_function(self):
		return self.function

	def get_request(self):
		return self.request

	def get_temporal_moment(self):
		return self.temporalMoment