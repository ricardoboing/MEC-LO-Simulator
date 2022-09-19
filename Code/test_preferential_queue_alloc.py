from simulator.Simulation import *
from distributor.TestDistributor import *

from scenario_object.Request import *
from scenario_object.Service import *
from queue_algorithm.preferential_queue.PreferentialQueue import *

_queue = PreferentialQueue()
requestList = []

def push_request(generatedTime, serviceMaxProcessTime, serviceDeadline):
	service = Service("", serviceDeadline, serviceMaxProcessTime)
	request = Request(None, None, service, generatedTime)

	succes = _queue.push_request(request)
	requestList.append(request)

	return succes

def assert_block(block, noneLeft, noneRight):
	if noneLeft:
		assert block.leftBlock == None
	else:
		assert block.leftBlock.rightBlock == block

	if noneRight:
		assert block.rightBlock == None
	else:
		assert block.rightBlock.leftBlock == block

def assert_free_block(block, start, end, noneLeft, noneRight):
	print("B", block.start, block.end)
	assert block.__class__ == FreeBlock
	assert block.start == start
	assert block.end == end

	assert_block(block, noneLeft, noneRight)

	return block.rightBlock

def assert_request_block(block, start, end, request, noneLeft, noneRight):
	print("R", block.start, block.end)
	assert block.__class__ == RequestBlock
	assert block.start == start
	assert block.end == end
	assert block.request == request

	assert_block(block, noneLeft, noneRight)

	return block.rightBlock

def default_assert(lastBlock):
	assert lastBlock == _queue.lastBlock
	assert _queue.firstBlock.leftBlock == None
	assert _queue.lastBlock.rightBlock == None

def test_1():
	print("Test 1 - First request")
	assert push_request(5, 10, 15) == True
	
	block = _queue.firstBlock
	block = assert_free_block(block, 0, 10, True, False)
	# R1
	block = assert_request_block(block, 10, 20, requestList[0], False, False)
	assert_free_block(block, 20, math.inf, False, True)

	default_assert(block)

def test_2():
	print("Test 2 - No conflict")
	Simulation._set_clock_pointer(5)
	assert push_request(10, 2, 50) == True
	
	block = _queue.firstBlock
	block = assert_free_block(block, 5, 10, True, False)
	# R1
	block = assert_request_block(block, 10, 20, requestList[0], False, False)
	block = assert_free_block(block, 20, 58, False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	assert_free_block(block, 60, math.inf, False, True)

	default_assert(block)

def test_3():
	print("Test 3 - Left conflict")
	Simulation._set_clock_pointer(7)
	assert push_request(15, 10, 45) == True
	
	block = _queue.firstBlock
	block = assert_free_block(block, 7, 10, True, False)
	# R1
	block = assert_request_block(block, 10, 20, requestList[0], False, False)
	block = assert_free_block(block, 20, 48, False, False)
	# R3
	block = assert_request_block(block, 48, 58, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	assert_free_block(block, 60, math.inf, False, True)

	default_assert(block)

def test_4():
	print("Test 4 - No conflict")
	assert push_request(50, 15, 100) == True
	
	block = _queue.firstBlock
	block = assert_free_block(block, 7, 10, True, False)
	# R1
	block = assert_request_block(block, 10, 20, requestList[0], False, False)
	block = assert_free_block(block, 20, 48, False, False)
	# R3
	block = assert_request_block(block, 48, 58, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	block = assert_free_block(block, 60, 135, False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

def test_5():
	print("Test 5 - Left conflict")
	
	assert push_request(20, 15, 30) == True
	
	block = _queue.firstBlock
	block = assert_free_block(block, 7, 10, True, False)
	# R1
	block = assert_request_block(block, 10, 20, requestList[0], False, False)
	block = assert_free_block(block, 20, 33, False, False)
	# R5
	block = assert_request_block(block, 33, 48, requestList[4], False, False)
	# R3
	block = assert_request_block(block, 48, 58, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	block = assert_free_block(block, 60, 135, False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

def test_6():
	print("Test 6 - No add")
	assert push_request(10, 20, 24) == False
	Simulation._set_clock_pointer(8)
	
	block = _queue.firstBlock
	block = assert_free_block(block, 7, 10, True, False)
	# R1
	block = assert_request_block(block, 10, 20, requestList[0], False, False)
	block = assert_free_block(block, 20, 33, False, False)
	# R5
	block = assert_request_block(block, 33, 48, requestList[4], False, False)
	# R3
	block = assert_request_block(block, 48, 58, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	block = assert_free_block(block, 60, 135, False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

def test_7():
	print("Test 7 - Back in time")

	notBack = False

	try:
		Simulation._set_clock_pointer(2)
	except:
		notBack = True

	assert notBack == True

if __name__ == "__main__":
	Simulation(TestDistributor)

	test_1()
	test_2()
	test_3()
	test_4()
	test_5()
	test_6()
	test_7()

	print("All tests are ok")