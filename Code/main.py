from file.file_name.input import *
from scenario_object.Scenario import *

from simulator.Simulation import *
from distributor.distributor_type_list import *

def get_copy_request_list(requestList):
	copyRequestList = []

	for request in requestList:
		requestClone = request.get_a_clone()
		copyRequestList.append(requestClone)

	return copyRequestList

def main():
	scenario = Scenario(FILE_NAME_SCENARIO_1)
	requestList = scenario.get_request_object_list()
	mecList = scenario.get_mec_list()

	Simulation.set_mec_list(mecList)

	for distributor in DistributorAlgorithm:
		copyRequestList = get_copy_request_list(requestList)

		Simulation(distributor)
		Simulation.generate_initial_user_event_list(copyRequestList)
		Simulation.start()

if __name__ == "__main__":
	main()