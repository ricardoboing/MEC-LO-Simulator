from file.file_name.input import *
from scenario_object.Scenario import *

from simulator.Simulation import *
from distributor.distributor_type_list import *
from file.output_scenario_writer.OutputScenarioWriter import *

def get_copy_request_list(requestList):
	copyRequestList = []

	for request in requestList:
		requestClone = request.get_a_clone()
		copyRequestList.append(requestClone)

	return copyRequestList

def simulate_scenario(scenario):
	requestList = scenario.get_request_object_list()
	mecList = scenario.get_mec_list()

	Simulation.set_mec_list(mecList)

	for distributor in DistributorAlgorithm:
		copyRequestList = get_copy_request_list(requestList)

		Simulation(distributor)
		Simulation.generate_initial_user_event_list(copyRequestList)
		Simulation.start()

def writer_output_file(outputFileName):
	writer = OutputScenarioWriter(outputFileName)

	simulationLogList = Logger.get_simulation_log_list()

	for simulationLog in simulationLogList:
		periodLogList = simulationLog.get_period_log_list()

		distributorSheetName = simulationLog.get_distributor_class().__name__
		writer.create_distributor_sheet(distributorSheetName)

		for periodLog in periodLogList:
			writer.set_row_in_distributor_sheet(
				periodLog.get_time(),
				periodLog.get_success_counter(),
				periodLog.get_fail_counter(),
				periodLog.get_network_counter()
			)
			writer.set_row_in_success_sheet(
				periodLog.get_time(),
				periodLog.get_success_counter()
			)
			writer.set_row_in_fail_sheet(
				periodLog.get_time(),
				periodLog.get_fail_counter()
			)
			writer.set_row_in_network_sheet(
				periodLog.get_time(),
				periodLog.get_network_counter()
			)
			'''
			print(
				periodLog.get_time(),
				periodLog.get_network_counter(),
				periodLog.get_success_counter(),
				periodLog.get_fail_counter()
			)
			'''
			writer.increment_row_index()

	writer.save()

def main():
	scenario = Scenario(FILE_NAME_SCENARIO_1)
	simulate_scenario(scenario)
	writer_output_file("output.xlsx")

	pass

if __name__ == "__main__":
	main()