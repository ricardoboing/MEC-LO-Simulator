from simulator.Simulation import *
from scenario_object.User import User

def generate_event_user_receive_response_request(requestPackage):
	delay = Simulation.get_network_mec_user_delay()
	eventFunction = User.receive_response_request

	return SimulatorEvent.generate_new_event(eventFunction, requestPackage, delay)

def generate_event_mec_receive_forward_request(requestPackage):
	DistributorType = Simulation.get_distributor_type()

	delay = Simulation.get_network_mec_mec_delay()
	eventFunction = DistributorType.receive_forward_request

	return SimulatorEvent.generate_new_event(eventFunction, requestPackage, delay)

def generate_event_finish_request_processing(requestPackage):
	pass

def generate_event_interrupt_request_processing(requestPackage):
	pass

class Distributor:
	@staticmethod
	def send_forward_request(packageRequest):
		Simulation.increment_network_traffic()

		event = generate_event_mec_receive_forward_request(packageRequest)
		return [event]

	@staticmethod
	def send_user_response_request(packageRequest):
		Simulation.increment_network_traffic()

		event = generate_event_user_receive_response_request(packageRequest)
		return [event]

	@staticmethod
	def receive_user_request(DistributorType, packageRequest):
		return DistributorType.send_user_response_request(packageRequest)

	@staticmethod
	def receive_forward_request(DistributorType, packageRequest):
		return DistributorType.send_forward_request(packageRequest)
