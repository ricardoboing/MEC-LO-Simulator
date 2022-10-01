from simulator.Simulation import *
from distributor.OriginalSequentialForwarding import *

from scenario_object.Request import *
from scenario_object.Service import *
from queue_algorithm.preferential_queue.PreferentialQueue import *

_queue = PreferentialQueue()
requestList = []

def reset():
	global requestList
	_queue = PreferentialQueue()
	requestList = []
	Simulation._currentSimulation.clockPointer = 0

def get_request():
	return _queue.get_first_request()

def push_request(generatedTime, serviceMaxProcessTime, serviceDeadline, force=False):
	service = Service("", serviceDeadline, serviceMaxProcessTime)
	request = Request(None, None, service, generatedTime)

	succes = _queue.push_request(request, force)
	if succes:
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
	print("B", block.start, block.end, block.__class__.__name__)
	assert block.__class__ == FreeBlock
	assert block.start == start
	assert block.end == end

	assert_block(block, noneLeft, noneRight)

	return block.rightBlock

def assert_request_block(block, start, end, request, noneLeft, noneRight):
	print("R", block.start, block.end, block.__class__.__name__)
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

def test_0():
	assert _queue.is_empty() == True

def test_1():
	print("Test 1 (alloc) - First request")
	assert push_request(5, 10, 15) == True
	
	block = _queue.firstBlock
	block = assert_free_block(block, 0, 10, True, False)
	# R1
	block = assert_request_block(block, 10, 20, requestList[0], False, False)
	assert_free_block(block, 20, math.inf, False, True)

	default_assert(block)

def test_2():
	print("Test 2 (alloc) - No conflict")
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
	print("Test 3 (alloc) - Left conflict")
	Simulation._set_clock_pointer(6)
	assert push_request(15, 10, 45) == True
	
	block = _queue.firstBlock
	block = assert_free_block(block, 6, 10, True, False)
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
	print("Test 4 (alloc) - No conflict")
	assert push_request(50, 15, 100) == True
	
	block = _queue.firstBlock
	block = assert_free_block(block, 6, 10, True, False)
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
	print("Test 5 (alloc) - Left conflict")
	
	assert push_request(20, 15, 30) == True
	
	block = _queue.firstBlock
	block = assert_free_block(block, 6, 10, True, False)
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
	print("Test 6 (alloc) - No add and no update the first block")
	assert push_request(10, 20, 24) == False
	Simulation._set_clock_pointer(7)
	
	block = _queue.firstBlock
	block = assert_free_block(block, 6, 10, True, False)
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

def test_8():
	print("Test 8 (dealloc)")
	request = get_request()
	assert request == requestList[0]

	block = _queue.firstBlock
	block = assert_free_block(block, 17, 33, True, False)
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

	Simulation._set_clock_pointer(17)

def test_9():
	print("Test 9 (dealloc)")
	request = get_request()
	assert request == requestList[4]

	block = _queue.firstBlock
	block = assert_free_block(block, 32, 48, True, False)
	# R3
	block = assert_request_block(block, 48, 58, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	block = assert_free_block(block, 60, 135, False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

	Simulation._set_clock_pointer(32)

def test_10():
	print("Test 10 (alloc) left conflict")
	assert push_request(29, 10, 20) == True

	block = _queue.firstBlock
	block = assert_free_block(block, 32, 38, True, False)
	# R6
	block = assert_request_block(block, 38, 48, requestList[5], False, False)
	# R3
	block = assert_request_block(block, 48, 58, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	block = assert_free_block(block, 60, 135, False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

def test_11():
	print("Test 11 (dealloc)")
	request = get_request()
	assert request == requestList[5]

	block = _queue.firstBlock
	block = assert_free_block(block, 42, 48, True, False)
	# R3
	block = assert_request_block(block, 48, 58, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	block = assert_free_block(block, 60, 135, False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

	Simulation._set_clock_pointer(42)

def test_12():
	print("Test 12 alloc")
	assert push_request(40, 1, 4) == True

	block = _queue.firstBlock
	block = assert_free_block(block, 42, 43, True, False)
	# R7
	block = assert_request_block(block, 43, 44, requestList[6], False, False)
	block = assert_free_block(block, 44, 48, False, False)
	# R3
	block = assert_request_block(block, 48, 58, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	block = assert_free_block(block, 60, 135, False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

def test_13():
	print("Test 13 dealloc")
	request = get_request()
	assert request == requestList[6]

	block = _queue.firstBlock
	block = assert_free_block(block, 43, 48, True, False)
	# R3
	block = assert_request_block(block, 48, 58, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	block = assert_free_block(block, 60, 135, False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

	Simulation._set_clock_pointer(43)

def test_14():
	print("Test 14 alloc")
	assert push_request(42, 4, 5) == True

	block = _queue.firstBlock
	# R8
	block = assert_request_block(block, 43, 47, requestList[7], True, False)
	block = assert_free_block(block, 47, 48, False, False)
	# R3
	block = assert_request_block(block, 48, 58, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	block = assert_free_block(block, 60, 135, False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

def test_15():
	print("Test 15 dealloc")
	request = get_request()
	assert request == requestList[7]

	block = _queue.firstBlock
	block = assert_free_block(block, 47, 48, True, False)
	# R3
	block = assert_request_block(block, 48, 58, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	block = assert_free_block(block, 60, 135, False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

	Simulation._set_clock_pointer(47)

def test_16():
	print("Test 16 dealloc")
	request = get_request()
	assert request == requestList[2]

	block = _queue.firstBlock
	block = assert_free_block(block, 57, 58, True, False)
	# R2
	block = assert_request_block(block, 58, 60, requestList[1], False, False)
	block = assert_free_block(block, 60, 135, False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

	Simulation._set_clock_pointer(57)

def test_17():
	print("Test 17 dealloc")
	request = get_request()
	assert request == requestList[1]

	block = _queue.firstBlock
	block = assert_free_block(block, 59, 135, True, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

	Simulation._set_clock_pointer(59)

def test_18():
	print("Test 18 dealloc")
	request = get_request()
	assert request == requestList[3]

	block = _queue.firstBlock
	assert_free_block(block, 74, math.inf, True, True)

	default_assert(block)

	Simulation._set_clock_pointer(74)

def test_19():
	print("Test 19 alloc")
	assert push_request(75, 5, 10) == True
	
	block = _queue.firstBlock
	block = assert_free_block(block, 74, 80, True, False)
	# R9
	block = assert_request_block(block, 80, 85, requestList[8], False, False)
	assert_free_block(block, 85, math.inf, False, True)

	default_assert(block)

def test_20():
	print("Test 20 dealloc")
	request = get_request()
	assert request == requestList[8]

	block = _queue.firstBlock
	assert_free_block(block, 79, math.inf, True, True)

	default_assert(block)

	Simulation._set_clock_pointer(79)

def test_21():
	print("Test 21 alloc")
	assert push_request(79, 10, 10) == True
	
	block = _queue.firstBlock
	# R10
	block = assert_request_block(block, 79, 89, requestList[9], True, False)
	assert_free_block(block, 89, math.inf, False, True)

	default_assert(block)

def test_22():
	print("Test 22 dealloc")
	request = get_request()
	assert request == requestList[9]

	block = _queue.firstBlock
	assert_free_block(block, 89, math.inf, True, True)

	default_assert(block)

	Simulation._set_clock_pointer(89)

def test_23():
	print("Test 23 deadline overflow and not force")
	assert push_request(75, 5, 10) == False

def test_24():
	print("Test 24 deadline overflow and force")
	assert push_request(75, 5, 10, True) == True

	block = _queue.firstBlock
	# R11
	block = assert_request_block(block, 89, 94, requestList[10], True, False)
	assert_free_block(block, 94, math.inf, False, True)

	default_assert(block)

def test_25():
	print("Test 25 deadline overflow and force")
	assert push_request(75, 5, 10, True) == True

	block = _queue.firstBlock
	# R11
	block = assert_request_block(block, 89, 94, requestList[10], True, False)
	# R12
	block = assert_request_block(block, 94, 99, requestList[11], False, False)
	assert_free_block(block, 99, math.inf, False, True)

	default_assert(block)

def test_26():
	print("Test 26")
	request = get_request()
	assert request == requestList[10]

	block = _queue.firstBlock
	# R12
	block = assert_request_block(block, 94, 99, requestList[11], True, False)
	assert_free_block(block, 99, math.inf, False, True)

	default_assert(block)

	Simulation._set_clock_pointer(94)

def test_27():
	print("Test 27")
	request = get_request()
	assert request == requestList[11]

	block = _queue.firstBlock
	assert_free_block(block, 99, math.inf, True, True)

	default_assert(block)

	Simulation._set_clock_pointer(99)

def test_28():
	print("Test 28")
	assert push_request(10, 80, 140) == True
	
	block = _queue.firstBlock
	block = assert_free_block(block, 6, 10, True, False)
	# R1
	block = assert_request_block(block, 10, 20, requestList[0], False, False)
	block = assert_free_block(block, 20, 28, False, False)
	# R5
	block = assert_request_block(block, 28, 43, requestList[4], False, False)
	# R3
	block = assert_request_block(block, 43, 53, requestList[2], False, False)
	# R2
	block = assert_request_block(block, 53, 55, requestList[1], False, False)
	# R6
	block = assert_request_block(block, 55, 135, requestList[5], False, False)
	# R4
	block = assert_request_block(block, 135, 150, requestList[3], False, False)
	assert_free_block(block, 150, math.inf, False, True)

	default_assert(block)

if __name__ == "__main__":
	Simulation(OriginalSequentialForwarding)

	test_0()
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
	test_18()
	test_19()
	test_20()

	test_21()
	test_22()
	test_0()

	test_23()
	test_24()
	test_25()
	test_26()
	test_27()

	reset()

	test_0()
	test_1()
	test_2()
	test_3()
	test_4()
	test_5()
	test_28()

	print("All tests are ok")