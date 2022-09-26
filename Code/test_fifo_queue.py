from simulator.Simulation import *
from distributor.OriginalSequentialForwarding import *

from scenario_object.Request import *
from scenario_object.Service import *

from queue_algorithm.Fifo import *

_queue = Fifo()

def get_request():
	return _queue.get_first_request()

def push_request(generatedTime, serviceMaxProcessTime, serviceDeadline, force):
	service = Service("", serviceDeadline, serviceMaxProcessTime)
	request = Request(None, None, service, generatedTime)

	return _queue.push_request(request, force)

def test_0():
	print("Test 0 - is_empty")
	assert _queue.is_empty() == True
	assert len(_queue.queue) == 0

def test_1():
	print("Test 1 - push first")
	assert push_request(5, 10, 15, False) == True
	assert len(_queue.queue) == 1

def test_2():
	print("Test 2 - push second")
	assert push_request(5, 10, 15, False) == True
	assert len(_queue.queue) == 2

def test_3():
	print("Test 3 - not push")
	assert push_request(5, 10, 15, False) == False
	assert len(_queue.queue) == 2

def test_4():
	print("Test 4 - pop first")
	assert get_request()
	assert len(_queue.queue) == 1

def test_5():
	print("Test 5 - move clock and not push")
	Simulation._set_clock_pointer(10)
	assert push_request(5, 10, 15, False) == False

def test_6():
	print("Test 6 - pop first")
	assert get_request()
	assert len(_queue.queue) == 0

def test_7():
	print("Test 7 - move clock and not push")
	Simulation._set_clock_pointer(20)
	assert push_request(5, 10, 15, False) == False

def test_8():
	print("Test 8 - move clock and push with deadline overflow")
	Simulation._set_clock_pointer(20)
	assert push_request(5, 10, 15, True) == True

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

	print("All tests are ok")