from simulator.Simulation import *

def generate_event_receive_user_request(requestPackage):
	DistributorType = Simulation.get_distributor_type()

	delay = Simulation.get_network_user_mec_delay()
	eventFunction = DistributorType.receive_user_request

	return SimulatorEvent.generate_new_event(eventFunction, requestPackage, delay)

class User:
	@staticmethod
	def receive_response_request(requestPackage):
		#print("User.receive_response_request", requestPackage.get_request().get_id())

		request = requestPackage.get_request()
		request.set_responsed()

		if request.met_the_deadline():
			#print("??")
			Simulation.increment_success_counter()
		else:
			Simulation.increment_fail_counter()

	@staticmethod
	def send_request_package(requestPackage):
		#print("User.send_request_package", requestPackage.get_request().get_id())
		Simulation.increment_network_traffic()

		event = generate_event_receive_user_request(requestPackage)
		return [event]