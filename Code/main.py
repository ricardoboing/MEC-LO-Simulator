from file.file_name.input import *
from scenario_object.Scenario import *

from simulator.Simulation import *
from distributor.DistributorAlgorithm import *

def get_copy_request_list(requestList):
	copyRequestList = []

	for request in requestList:
		requestClone = request.get_a_clone()
		copyRequestList.append(requestClone)

	return copyRequestList

def main():
	scenario = Scenario(FILE_NAME_SCENARIO_1)
	requestList = scenario.get_request_object_list()

	for distributor in DistributorAlgorithm:
		copyRequestList = get_copy_request_list(requestList)

		simulation = Simulation(distributor)
		simulation.generate_initial_user_event_list(copyRequestList)
		simulation.start()

if __name__ == "__main__":
	main()