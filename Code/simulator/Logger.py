class _PeriodLog:
	def __init__(self, time):
		self.time = time
		self.successCounter = 0
		self.failCounter = 0

	def increment_success_counter(self):
		self.successCounter += 1

	def increment_fail_counter(self):
		self.failCounter += 1

	def get_success_counter(self):
		return self.successCounter

	def get_fail_counter(self):
		return self.failCounter

class SimulationLog:
	def __init__(self, intervalBetweenLog):
		self.intervalBetweenLog = intervalBetweenLog
		self.periodLogList = []

	def create_new_period_log(self):
		pass

	def get_current_period_log(self, time):
		return self.periodLogList[-1]

class Logger:
	_SimulationLogList = []
	_IntervalBetweenLog = -1

	@staticmethod
	def set_interval_between_log(intervalBetweenLog):
		Logger._IntervalBetweenLog = intervalBetweenLog

	@staticmethod
	def create_new_simulation_log():
		Logger._SimulationLogList.append( SimulationLog(Logger._IntervalBetweenLog) )

	@staticmethod
	def increment_success_counter():
		pass

	@staticmethod
	def increment_fail_counter():
		pass

	@staticmethod
	def get_simulation_log_list():
		return Logger._SimulationLogList