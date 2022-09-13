class Service:
	def __init__(self, name, deadline, maxProcessTime):
		self.name = name
		self.deadline = deadline
		self.maxProcessTime = maxProcessTime

	def get_name(self):
		return self.name

	def get_deadline(self):
		return self.deadline

	def get_max_process_time(self):
		return self.maxProcessTime