from simulator.Simulation import *
from queue_algorithm.RequestQueue import *
from queue_algorithm.preferential_queue.RequestBlock import *
import math

def _get_useful_area(leftBlock, newBlock, rightBlock, cpuFreeTime):
	if leftBlock != None:
		start = leftBlock.get_end()
	else:
		start = cpuFreeTime

	if rightBlock != None:
		end = rightBlock.get_start()
	else:
		end = math.inf

	end = min(end, newBlock.get_end())
	
	if start > end:
		start = 0
		end = 0

	width = end - start

	return Block(width, end)

def _create_request_block(request):
	service = request.get_service()
	serviceDeadline = service.get_deadline()

	serviceMaxProcessTime = service.get_max_process_time()
	requestGenerated = request.get_generated_time()

	end = requestGenerated + serviceDeadline
	width = serviceMaxProcessTime

	return RequestBlock(width, end, request)

def _shift_left(block, shiftValue):
	end = block.get_end() - shiftValue
	block.set_end(end)

class PreferentialQueue(RequestQueue):
	def __init__(self):
		self.firstBlock = None
		self.lastBlock = None

	def push_request(self, request, cpuFreeTime, forcedPush):
		newBlock = _create_request_block(request)

		leftBlock = self.lastBlock
		if leftBlock != None:
			assert leftBlock.get_right_block() == None
		rightBlock = None

		spaceNeeded = newBlock.get_size()
		hasRightSpace = False

		status = self._search_alloc_space(leftBlock, newBlock, rightBlock, spaceNeeded, hasRightSpace, cpuFreeTime, forcedPush)

		if status:
			return True
		if not forcedPush:
			return False

		if self.is_empty():
			start = cpuFreeTime
		else:
			start = leftBlock.end

		end = start + spaceNeeded
		newBlock.set_end(end)

		self._alloc_request(leftBlock, newBlock, rightBlock)
		return True

	def _alloc_request(self, leftBlock, newBlock, rightBlock):
		if leftBlock != None:
			leftBlock.set_right_block(newBlock)
		else:
			self.firstBlock = newBlock

		if rightBlock != None:
			rightBlock.set_left_block(newBlock)
		else:
			self.lastBlock = newBlock

		newBlock.set_left_block(leftBlock)
		newBlock.set_right_block(rightBlock)

	def _shift_or_alloc(self, leftBlock, newBlock, rightBlock, end, spaceNeeded, hasRightSpace):
		if hasRightSpace:
			_shift_left(rightBlock, spaceNeeded)
		else:
			if newBlock.get_right_block() == None and newBlock.get_left_block() == None:
				newBlock.set_end(end)
				self._alloc_request(leftBlock, newBlock, rightBlock)

	def _search_alloc_space(self, leftBlock, newBlock, rightBlock, spaceNeeded, hasRightSpace, cpuFreeTime, forcedPush):
		usefulArea = _get_useful_area(leftBlock, newBlock, rightBlock, cpuFreeTime)

		end = usefulArea.get_end()
		freeSpace = usefulArea.get_size()
		
		if freeSpace >= spaceNeeded:
			self._shift_or_alloc(leftBlock, newBlock, rightBlock, end, spaceNeeded, hasRightSpace)
			return True

		if leftBlock == None:
			if forcedPush and rightBlock != None:
				shiftValue = rightBlock.get_start() - cpuFreeTime
				_shift_left(rightBlock, shiftValue)
			return False

		if freeSpace > 0:
			_hasRightSpace = True
		else:
			_hasRightSpace = hasRightSpace

		_freeNeeded = spaceNeeded - freeSpace
		_leftBlock = leftBlock.get_left_block()
		_rightBlock = leftBlock

		status = self._search_alloc_space(_leftBlock, newBlock, _rightBlock, _freeNeeded, _hasRightSpace, cpuFreeTime, forcedPush)

		if not status:
			if forcedPush and rightBlock != None:
				shiftValue = rightBlock.get_start() - leftBlock.get_end()
				_shift_left(rightBlock, shiftValue)
			return False

		self._shift_or_alloc(leftBlock, newBlock, rightBlock, end, spaceNeeded, hasRightSpace)
		return True

	def get_first_request(self):
		assert not self.is_empty()

		block = self.firstBlock
		self.firstBlock = self.firstBlock.get_right_block()

		if self.firstBlock != None:
			self.firstBlock.set_left_block(None)
		else:
			self.lastBlock = None

		return block.get_request()

	def is_empty(self):
		if self.firstBlock == None or self.lastBlock == None:
			assert self.firstBlock == self.lastBlock

		return self.firstBlock == None and self.lastBlock == None