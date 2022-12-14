from simulator.EventScheduler import *
from simulator.SimulatorEvent import *
from simulator.RequestPackage import *
from simulator.Logger import *

def reset_mec_list(mecList, QueueClass):
	for mec in mecList:
		mec.reset()
		mec.set_a_new_request_queue(QueueClass)

class Simulation:
	_currentSimulation = None
	_mecList = None

	def __init__(self, DistributorClass):
		self.DistributorClass = DistributorClass
		self.eventScheduler = EventScheduler()
		self.clockPointer = 0
		self.networkTraffic = 0

		Simulation._currentSimulation = self

	@staticmethod
	def start():
		currentSimulation = Simulation._currentSimulation
		DistributorClass = currentSimulation.DistributorClass
		QueueClass = DistributorClass.QueueClass
		reset_mec_list(Simulation._mecList, QueueClass)
		Logger.create_new_simulation_log(DistributorClass)

		while not currentSimulation.eventScheduler.is_empty():
			event = currentSimulation.eventScheduler.get_next_event()
			temporalMoment = event.get_temporal_moment()
			
			currentSimulation._set_clock_pointer(temporalMoment)
			newEventList = event.happen()

			currentSimulation.eventScheduler.push_event_list(newEventList)

	@staticmethod
	def generate_initial_user_event_list(requestList):
		from scenario_object.User import User

		currentSimulation = Simulation._currentSimulation

		for request in requestList:
			destination = request.get_first_mec_destination()
			package = RequestPackage(request, destination)
			delay = request.get_generated_time()

			event = SimulatorEvent.generate_new_event(User.send_request_package, package, delay)
			currentSimulation.eventScheduler.push_event(event)

	@staticmethod
	def increment_network_traffic():
		Logger.increment_network_counter()

	@staticmethod
	def increment_success_counter():
		Logger.increment_success_counter()

	@staticmethod
	def increment_fail_counter():
		Logger.increment_fail_counter()

	def increment_forward_counter():
		Logger.increment_forward_counter()

	@staticmethod
	def set_mec_list(mecList):
		Simulation._mecList = mecList

	@staticmethod
	def _set_clock_pointer(newPointer):
		if newPointer < Simulation._currentSimulation.clockPointer:
			raise Exception("newPointer < self.clockPointer in Simulation class.")

		Simulation._currentSimulation.clockPointer = newPointer

	def get_mec_list():
		return Simulation._mecList

	@staticmethod
	def get_distributor_type():
		return Simulation._currentSimulation.DistributorClass

	@staticmethod
	def get_clock_pointer():
		return Simulation._currentSimulation.clockPointer

	@staticmethod
	def get_network_user_mec_delay():
		return 0

	@staticmethod
	def get_network_mec_mec_delay():
		return 0

	@staticmethod
	def get_network_mec_user_delay():
		return 0