class Service:
	def __init__(self, deadline, maxProcessTime):
		self.deadline = deadline
		self.maxProcessTime = maxProcessTime

	def get_deadline(self):
		return self.deadline

	def get_max_process_time(self):
		return self.maxProcessTime