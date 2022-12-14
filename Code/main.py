from file.file_name.input import *
from file.file_name.output import *
from scenario_object.Scenario import *

from simulator.Simulation import *
from distributor.distributor_type_list import *
from file.output_scenario_writer.OutputScenarioWriter import *

import datetime

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
				periodLog.get_network_counter(),
				periodLog.get_forward_counter()
			)

			writer.increment_row_index()

	writer.save()

def get_a_new_output_name(fileName):
	dateStr = str(datetime.datetime.now()) + "___"
	dateStr = dateStr.replace(" ", "_")
	dateStr = dateStr.replace("-", "_")
	dateStr = dateStr.replace(":", "_")
	dateStr = dateStr.replace(".", "_")

	return OUTPUT_SRC + dateStr + fileName

def main():
	fileName = INPUT_FILE_NAME_SCENARIO_1

	inputFileSrc = INPUT_SRC + fileName
	scenario = Scenario(inputFileSrc)
	simulate_scenario(scenario)

	print("Saving output file...")
	outputFileName = get_a_new_output_name(fileName)
	writer_output_file(outputFileName)

if __name__ == "__main__":
	main()