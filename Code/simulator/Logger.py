import math

class _PeriodLog:
	def __init__(self, time):
		self.time = time
		self.successCounter = 0
		self.failCounter = 0
		self.networkTraffic = 0
		self.forwardCounter = 0

	def increment_success_counter(self):
		self.successCounter += 1

	def increment_fail_counter(self):
		self.failCounter += 1

	def increment_network_counter(self):
		self.networkTraffic += 1

	def increment_forward_counter(self):
		self.forwardCounter += 1

	def get_time(self):
		return self.time

	def get_success_counter(self):
		return self.successCounter

	def get_fail_counter(self):
		return self.failCounter

	def get_network_counter(self):
		return self.networkTraffic

	def get_forward_counter(self):
		return self.forwardCounter

	def get_clone(self, time):
		clone = _PeriodLog(time)
		clone.successCounter = self.successCounter
		clone.failCounter = self.failCounter
		clone.networkTraffic = self.networkTraffic
		clone.forwardCounter = self.forwardCounter

		return clone

class SimulationLog:
	def __init__(self, DistributorClass, intervalBetweenLog):
		self.DistributorClass = DistributorClass
		self.intervalBetweenLog = intervalBetweenLog
		self.periodLogList = []

		self.currentPeriodLog = _PeriodLog(0)

	def increment_success_counter(self):
		self._check_period_log()
		self.currentPeriodLog.increment_success_counter()

	def increment_fail_counter(self):
		self._check_period_log()
		self.currentPeriodLog.increment_fail_counter()

	def increment_network_counter(self):
		self._check_period_log()
		self.currentPeriodLog.increment_network_counter()

	def increment_forward_counter(self):
		self._check_period_log()
		self.currentPeriodLog.increment_forward_counter()

	def get_distributor_class(self):
		return self.DistributorClass

	def get_period_log_list(self):
		return self.periodLogList

	def _check_period_log(self):
		from simulator.Simulation import Simulation
		
		realTime = Simulation.get_clock_pointer()
		currentIndex = self.currentPeriodLog.get_time()
		nextIndex = currentIndex + self.intervalBetweenLog

		if realTime >= nextIndex:
			i = math.floor(realTime / self.intervalBetweenLog)
			newPeriodLogTime = i * self.intervalBetweenLog

			self._create_new_period_log(newPeriodLogTime)

	def _create_new_period_log(self, time):
		newPeriodLog = self.currentPeriodLog.get_clone(time)

		self.currentPeriodLog = newPeriodLog
		self.periodLogList.append(newPeriodLog)

class Logger:
	_simulationLogList = []
	_intervalBetweenLog = 5 #################### <<<<<< 
	_currentSimulationLog = None

	@staticmethod
	def set_interval_between_log(intervalBetweenLog):
		Logger._intervalBetweenLog = intervalBetweenLog

	@staticmethod
	def create_new_simulation_log(DistributorClass):
		newSimulationLog = SimulationLog(DistributorClass, Logger._intervalBetweenLog)
		
		Logger._currentSimulationLog = newSimulationLog
		Logger._simulationLogList.append(newSimulationLog)

	@staticmethod
	def increment_success_counter():
		Logger._currentSimulationLog.increment_success_counter()

	@staticmethod
	def increment_fail_counter():
		Logger._currentSimulationLog.increment_fail_counter()

	@staticmethod
	def increment_network_counter():
		Logger._currentSimulationLog.increment_network_counter()

	@staticmethod
	def increment_forward_counter():
		Logger._currentSimulationLog.increment_forward_counter()

	@staticmethod
	def get_simulation_log_list():
		return Logger._simulationLogList