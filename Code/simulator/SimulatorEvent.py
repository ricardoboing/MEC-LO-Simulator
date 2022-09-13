class SimulatorEvent:
	def __init__(self, function, requestPackage):
		self.function = function
		self.requestPackage = requestPackage

	def happen(self):
		self.function( self.requestPackage )

	def get_temporal_moment(self):
		request = self.requestPackage.get_request()
		return request.get_generated_time()