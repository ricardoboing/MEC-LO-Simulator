from simulator.Simulation import *
from distributor.OriginalSequentialForwarding import *

from scenario_object.Request import *
from scenario_object.Service import *
from scenario_object.MecNode import *

from queue_algorithm.preferential_queue.PreferentialQueue import *

mec = MecNode("oi", 1)
requestList = [None]

def push_request(generatedTime, serviceDeadline, serviceMaxProcessTime, force=False):
	service = Service("", serviceDeadline, serviceMaxProcessTime)
	request = Request(None, None, service, generatedTime)

	succes = mec.receive_request(request, force)
	if succes:
		requestList.append(request)

	return succes

def assert_request_block(block, start, end, request, leftRequest, rightRequest):
	#print("R", block.start, block.end, block.__class__.__name__)
	assert block.__class__ == RequestBlock
	assert block.start == start
	assert block.end == end
	assert block.request == request

	if leftRequest == None:
		assert block.leftBlock == None
	else:
		assert block.leftBlock.get_request() == leftRequest
	
	if rightRequest == None:
		assert block.rightBlock == None
	else:
		assert block.rightBlock.get_request() == rightRequest

	return block.rightBlock

def default_assert(lastBlock):
	assert lastBlock == _queue.lastBlock
	assert _queue.firstBlock.leftBlock == None
	assert _queue.lastBlock.rightBlock == None

def test_1():
	print("test_1")
	assert _queue.is_empty() == True
	assert push_request(0, 20, 10) == True
	assert mec.freeCpuTime == 0
	
	block = _queue.firstBlock
	# R1
	block = assert_request_block(block, 10, 20, requestList[1], None, None)

def test_2():
	print("test_2")
	assert _queue.is_empty() == False
	assert push_request(5, 40, 20) == True
	assert mec.freeCpuTime == 0
	
	block = _queue.firstBlock
	# R1
	block = assert_request_block(block, 10, 20, requestList[1], None, requestList[2])
	# R2
	block = assert_request_block(block, 25, 45, requestList[2], requestList[1], None)

def test_3():
	print("test_3")
	assert _queue.is_empty() == False
	assert push_request(0, 70, 10) == True
	assert mec.freeCpuTime == 0
	
	block = _queue.firstBlock
	# R1
	block = assert_request_block(block, 10, 20, requestList[1], None, requestList[2])
	# R2
	block = assert_request_block(block, 25, 45, requestList[2], requestList[1], requestList[3])
	# R3
	block = assert_request_block(block, 60, 70, requestList[3], requestList[2], None)

def test_4():
	print("test_4")
	assert _queue.is_empty() == False
	assert push_request(0, 49, 10) == True
	assert mec.freeCpuTime == 0
	
	block = _queue.firstBlock
	# R1
	block = assert_request_block(block, 9, 19, requestList[1], None, requestList[2])
	# R2
	block = assert_request_block(block, 19, 39, requestList[2], requestList[1], requestList[4])
	# R4
	block = assert_request_block(block, 39, 49, requestList[4], requestList[2], requestList[3])
	# R3
	block = assert_request_block(block, 60, 70, requestList[3], requestList[4], None)

def test_5():
	print("test_5")
	assert _queue.is_empty() == False
	assert push_request(0, 55, 10) == True
	assert mec.freeCpuTime == 0
	
	block = _queue.firstBlock
	# R1
	block = assert_request_block(block, 5, 15, requestList[1], None, requestList[2])
	# R2
	block = assert_request_block(block, 15, 35, requestList[2], requestList[1], requestList[4])
	# R4
	block = assert_request_block(block, 35, 45, requestList[4], requestList[2], requestList[5])
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], requestList[4], requestList[3])
	# R3
	block = assert_request_block(block, 60, 70, requestList[3], requestList[5], None)

def test_6():
	print("test_6")
	assert _queue.is_empty() == False
	assert push_request(0, 10, 5) == True
	assert mec.freeCpuTime == 0
	
	block = _queue.firstBlock
	# R6
	block = assert_request_block(block, 0, 5, requestList[6], None, requestList[1])
	# R1
	block = assert_request_block(block, 5, 15, requestList[1], requestList[6], requestList[2])
	# R2
	block = assert_request_block(block, 15, 35, requestList[2], requestList[1], requestList[4])
	# R4
	block = assert_request_block(block, 35, 45, requestList[4], requestList[2], requestList[5])
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], requestList[4], requestList[3])
	# R3
	block = assert_request_block(block, 60, 70, requestList[3], requestList[5], None)

def test_7():
	print("test_7")
	assert _queue.is_empty() == False
	assert push_request(0, 75, 10) == True
	assert mec.freeCpuTime == 0
	
	block = _queue.firstBlock
	# R6
	block = assert_request_block(block, 0, 5, requestList[6], None, requestList[1])
	# R1
	block = assert_request_block(block, 5, 15, requestList[1], requestList[6], requestList[2])
	# R2
	block = assert_request_block(block, 15, 35, requestList[2], requestList[1], requestList[4])
	# R4
	block = assert_request_block(block, 35, 45, requestList[4], requestList[2], requestList[5])
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], requestList[4], requestList[3])
	# R3
	block = assert_request_block(block, 55, 65, requestList[3], requestList[5], requestList[7])
	# R7
	block = assert_request_block(block, 65, 75, requestList[7], requestList[3], None)

def test_8():
	print("test_8")
	assert _queue.is_empty() == False
	mec.start_next_request_processing()
	assert mec.freeCpuTime == 5
	
	block = _queue.firstBlock
	# R1
	block = assert_request_block(block, 5, 15, requestList[1], None, requestList[2])
	# R2
	block = assert_request_block(block, 15, 35, requestList[2], requestList[1], requestList[4])
	# R4
	block = assert_request_block(block, 35, 45, requestList[4], requestList[2], requestList[5])
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], requestList[4], requestList[3])
	# R3
	block = assert_request_block(block, 55, 65, requestList[3], requestList[5], requestList[7])
	# R7
	block = assert_request_block(block, 65, 75, requestList[7], requestList[3], None)

def test_9():
	print("test_9")
	assert _queue.is_empty() == False
	mec.finish_current_request_in_process()
	Simulation._set_clock_pointer(5)
	assert mec.freeCpuTime == 5
	mec.start_next_request_processing()
	assert mec.freeCpuTime == 15
	
	block = _queue.firstBlock
	# R2
	block = assert_request_block(block, 15, 35, requestList[2], None, requestList[4])
	# R4
	block = assert_request_block(block, 35, 45, requestList[4], requestList[2], requestList[5])
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], requestList[4], requestList[3])
	# R3
	block = assert_request_block(block, 55, 65, requestList[3], requestList[5], requestList[7])
	# R7
	block = assert_request_block(block, 65, 75, requestList[7], requestList[3], None)

def test_10():
	print("test_10")
	assert _queue.is_empty() == False
	mec.finish_current_request_in_process()
	Simulation._set_clock_pointer(15)
	assert mec.freeCpuTime == 15
	mec.start_next_request_processing()
	assert mec.freeCpuTime == 35
	
	block = _queue.firstBlock
	# R4
	block = assert_request_block(block, 35, 45, requestList[4], None, requestList[5])
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], requestList[4], requestList[3])
	# R3
	block = assert_request_block(block, 55, 65, requestList[3], requestList[5], requestList[7])
	# R7
	block = assert_request_block(block, 65, 75, requestList[7], requestList[3], None)

def test_11():
	print("test_11")
	assert _queue.is_empty() == False
	assert push_request(30, 65, 10) == True
	assert mec.freeCpuTime == 35
	
	block = _queue.firstBlock
	# R4
	block = assert_request_block(block, 35, 45, requestList[4], None, requestList[5])
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], requestList[4], requestList[3])
	# R3
	block = assert_request_block(block, 55, 65, requestList[3], requestList[5], requestList[7])
	# R7
	block = assert_request_block(block, 65, 75, requestList[7], requestList[3], requestList[8])
	# R8
	block = assert_request_block(block, 85, 95, requestList[8], requestList[7], None)

def test_12():
	print("test_12")
	assert _queue.is_empty() == False
	assert push_request(30, 70, 10) == True
	assert mec.freeCpuTime == 35
	
	block = _queue.firstBlock
	# R4
	block = assert_request_block(block, 35, 45, requestList[4], None, requestList[5])
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], requestList[4], requestList[3])
	# R3
	block = assert_request_block(block, 55, 65, requestList[3], requestList[5], requestList[7])
	# R7
	block = assert_request_block(block, 65, 75, requestList[7], requestList[3], requestList[8])
	# R8
	block = assert_request_block(block, 80, 90, requestList[8], requestList[7], requestList[9])
	# R9
	block = assert_request_block(block, 90, 100, requestList[9], requestList[8], None)

def test_13():
	print("test_13")
	assert _queue.is_empty() == False
	mec.finish_current_request_in_process()
	Simulation._set_clock_pointer(35)
	assert mec.freeCpuTime == 35
	mec.start_next_request_processing()
	assert mec.freeCpuTime == 45
	
	block = _queue.firstBlock
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], None, requestList[3])
	# R3
	block = assert_request_block(block, 55, 65, requestList[3], requestList[5], requestList[7])
	# R7
	block = assert_request_block(block, 65, 75, requestList[7], requestList[3], requestList[8])
	# R8
	block = assert_request_block(block, 80, 90, requestList[8], requestList[7], requestList[9])
	# R9
	block = assert_request_block(block, 90, 100, requestList[9], requestList[8], None)

def test_14():
	print("test_14")
	assert _queue.is_empty() == False
	assert push_request(40, 80, 10) == True
	assert mec.freeCpuTime == 45
	
	block = _queue.firstBlock
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], None, requestList[3])
	# R3
	block = assert_request_block(block, 55, 65, requestList[3], requestList[5], requestList[7])
	# R7
	block = assert_request_block(block, 65, 75, requestList[7], requestList[3], requestList[8])
	# R8
	block = assert_request_block(block, 80, 90, requestList[8], requestList[7], requestList[9])
	# R9
	block = assert_request_block(block, 90, 100, requestList[9], requestList[8], requestList[10])
	# R10
	block = assert_request_block(block, 110, 120, requestList[10], requestList[9], None)

def test_15():
	print("test_15")
	assert _queue.is_empty() == False
	assert push_request(40, 80, 20) == False
	assert mec.freeCpuTime == 45
	
	block = _queue.firstBlock
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], None, requestList[3])
	# R3
	block = assert_request_block(block, 55, 65, requestList[3], requestList[5], requestList[7])
	# R7
	block = assert_request_block(block, 65, 75, requestList[7], requestList[3], requestList[8])
	# R8
	block = assert_request_block(block, 80, 90, requestList[8], requestList[7], requestList[9])
	# R9
	block = assert_request_block(block, 90, 100, requestList[9], requestList[8], requestList[10])
	# R10
	block = assert_request_block(block, 110, 120, requestList[10], requestList[9], None)

def test_16():
	print("test_16")
	assert _queue.is_empty() == False
	assert push_request(40, 80, 20, True) == True
	assert mec.freeCpuTime == 45
	
	block = _queue.firstBlock
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], None, requestList[3])
	# R3
	block = assert_request_block(block, 55, 65, requestList[3], requestList[5], requestList[7])
	# R7
	block = assert_request_block(block, 65, 75, requestList[7], requestList[3], requestList[8])
	# R8
	block = assert_request_block(block, 75, 85, requestList[8], requestList[7], requestList[9])
	# R9
	block = assert_request_block(block, 85, 95, requestList[9], requestList[8], requestList[10])
	# R10
	block = assert_request_block(block, 95, 105, requestList[10], requestList[9], requestList[11])
	# R11
	block = assert_request_block(block, 105, 125, requestList[11], requestList[10], None)

def test_17():
	print("test_17")
	assert _queue.is_empty() == False
	assert push_request(40, 80, 20, True) == True
	assert mec.freeCpuTime == 45
	
	block = _queue.firstBlock
	# R5
	block = assert_request_block(block, 45, 55, requestList[5], None, requestList[3])
	# R3
	block = assert_request_block(block, 55, 65, requestList[3], requestList[5], requestList[7])
	# R7
	block = assert_request_block(block, 65, 75, requestList[7], requestList[3], requestList[8])
	# R8
	block = assert_request_block(block, 75, 85, requestList[8], requestList[7], requestList[9])
	# R9
	block = assert_request_block(block, 85, 95, requestList[9], requestList[8], requestList[10])
	# R10
	block = assert_request_block(block, 95, 105, requestList[10], requestList[9], requestList[11])
	# R11
	block = assert_request_block(block, 105, 125, requestList[11], requestList[10], requestList[12])
	# R11
	block = assert_request_block(block, 125, 145, requestList[12], requestList[11], None)

if __name__ == "__main__":
	Simulation(OriginalSequentialForwarding)

	global _queue
	_queue = mec.requestQueue = PreferentialQueue()

	test_1()
	test_2()
	test_3()
	test_4()

	test_5()
	test_6()
	test_7()
	test_8()

	test_9()
	test_10()
	test_11()
	test_12()
	test_13()

	test_14()
	test_15()
	test_16()
	test_17()

	print("All tests are ok")