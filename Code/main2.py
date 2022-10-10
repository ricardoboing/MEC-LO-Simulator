from main import *

def main2():
	fileName = INPUT_FILE_NAME_SCENARIO_1

	inputFileSrc = INPUT_SRC + fileName
	scenario = Scenario(inputFileSrc)

	distributorSummaryList = {}

	iterations = 40
	for i in range(0, iterations):
		print("iteration " + str(i))
		Logger._simulationLogList = []
		simulate_scenario(scenario)

		simulationLogList = Logger.get_simulation_log_list()

		for simulationLog in simulationLogList:
			distributorName = simulationLog.get_distributor_class().__name__
			periodLogList = simulationLog.get_period_log_list()

			lastLogList = periodLogList[-1]

			if distributorName not in distributorSummaryList:
				distributorSummaryList[distributorName] = {}
				distributorSummaryList[distributorName]["time"] = 0
				distributorSummaryList[distributorName]["success_counter"] = 0
				distributorSummaryList[distributorName]["fail_counter"] = 0
				distributorSummaryList[distributorName]["network_counter"] = 0
				distributorSummaryList[distributorName]["forward_counter"] = 0

			distributorSummaryList[distributorName]["time"] += lastLogList.get_time()
			distributorSummaryList[distributorName]["success_counter"] += lastLogList.get_success_counter()
			distributorSummaryList[distributorName]["fail_counter"] += lastLogList.get_fail_counter()
			distributorSummaryList[distributorName]["network_counter"] += lastLogList.get_network_counter()
			distributorSummaryList[distributorName]["forward_counter"] += lastLogList.get_forward_counter()

	print("Saving output file...")
	workbook = Workbook()

	for sheet in workbook:
		workbook.remove(sheet)

	sheet = workbook.create_sheet(title="summary")

	columnIndex = 1
	for distributorName in distributorSummaryList:
		columnIndex += 1
		columnLetter = get_column_letter(columnIndex)

		time = distributorSummaryList[distributorName]["time"] / iterations
		success = distributorSummaryList[distributorName]["success_counter"] / iterations
		fail = distributorSummaryList[distributorName]["fail_counter"] / iterations
		network = distributorSummaryList[distributorName]["network_counter"] / iterations
		forward = distributorSummaryList[distributorName]["forward_counter"] / iterations

		sheet["A"+str(2)].value = "time"
		sheet["A"+str(3)].value = "success"
		sheet["A"+str(4)].value = "fail"
		sheet["A"+str(5)].value = "network"
		sheet["A"+str(6)].value = "forward"

		sheet[columnLetter+str(1)].value = distributorName
		sheet[columnLetter+str(2)].value = time
		sheet[columnLetter+str(3)].value = success
		sheet[columnLetter+str(4)].value = fail
		sheet[columnLetter+str(5)].value = network
		sheet[columnLetter+str(6)].value = forward

	outputFileName = get_a_new_output_name(fileName)
	workbook.save(outputFileName)

if __name__ == "__main__":
	main2()