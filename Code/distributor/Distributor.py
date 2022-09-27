from simulator.Simulation import *
from scenario_object.User import User

import random

def generate_event_user_receive_response_request(request):
	delay = Simulation.get_network_mec_user_delay()
	eventFunction = User.receive_response_request

	requestPackage = RequestPackage(request, None)

	return SimulatorEvent.generate_new_event(eventFunction, requestPackage, delay)

def generate_event_mec_receive_forward_request(requestPackage):
	DistributorType = Simulation.get_distributor_type()

	delay = Simulation.get_network_mec_mec_delay()
	eventFunction = DistributorType.receive_forward_request

	return SimulatorEvent.generate_new_event(eventFunction, requestPackage, delay)

def generate_event_finish_request_processing(request, mec):
	DistributorType = Simulation.get_distributor_type()

	service = request.get_service()
	delay = service.get_max_process_time()
	eventFunction = Distributor.finish_current_request_processing

	return SimulatorEvent.generate_new_event(eventFunction, mec, delay)

def get_random_destination(visitedMecList):
	mecList = Simulation.get_mec_list()

	notVisitedList = []
	for mec in mecList:
		if mec not in visitedMecList:
			notVisitedList.append(mec)

	randomIndex = random.randint(0, len(notVisitedList)-1)

	return notVisitedList[randomIndex]

class Distributor:
	@staticmethod
	def send_forward_request(packageRequest):
		Simulation.increment_network_traffic()
		Simulation.increment_forward_counter()

		packageRequest.increment_forward_counter()
		visitedMecList = packageRequest.get_previous_destination_list()

		randomDestination = get_random_destination(visitedMecList)
		packageRequest.set_new_destination(randomDestination)

		event = generate_event_mec_receive_forward_request(packageRequest)
		return [event]

	@staticmethod
	def send_user_response_request(request):
		Simulation.increment_network_traffic()

		event = generate_event_user_receive_response_request(request)
		return [event]

	@staticmethod
	def finish_current_request_processing(mec):
		finishedRequest = mec.finish_current_request_in_process()

		eventList = Distributor.send_user_response_request(finishedRequest)
		eventList2 = Distributor.start_next_request_processing(mec)

		if eventList2 != None:
			eventList += eventList2

		return eventList

	@staticmethod
	def start_next_request_processing(mec):
		startedProcessing = mec.start_next_request_processing()

		if startedProcessing:
			currentRequest = mec.get_current_request_in_process()

			event = generate_event_finish_request_processing(currentRequest, mec)
			return [event]

		return None