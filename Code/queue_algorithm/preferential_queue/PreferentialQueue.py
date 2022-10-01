from simulator.Simulation import *
from queue_algorithm.preferential_queue.FreeBlock import *
from queue_algorithm.RequestQueue import *
import math

class PreferentialQueue(RequestQueue):
	def __init__(self):
		initialBlock = FreeBlock(0, math.inf)

		self.firstBlock = initialBlock
		self.lastBlock = initialBlock

	def push_request(self, request, forcedPush=False):
		self._update_first_freeblock()
		lastUtilBlock = get_last_util_block(self.lastBlock, request)

		if lastUtilBlock == None:
			if forcedPush:
				lastUtilBlock = self.lastBlock
			else:
				return False

		requestSize = get_request_size(request)

		if not forcedPush:
			hasSpace = has_space(lastUtilBlock, requestSize, request)
			
			if not hasSpace:
				return False

		rightBlock, areaShiftLeft = lastUtilBlock.alloc(request, forcedPush)
		shift_left(lastUtilBlock.get_left_block(), areaShiftLeft)

		if self.lastBlock == lastUtilBlock:
			self.lastBlock = rightBlock

		self.firstBlock = get_first_block(self.lastBlock)

		return True

	def get_first_request(self):
		if self.is_empty():
			return None

		if self.firstBlock.__class__ != RequestBlock:
			self.firstBlock = self.firstBlock.get_right_block()

		requestBlock = self.firstBlock
		secondBlock = self.firstBlock.get_right_block()

		realTime = Simulation.get_clock_pointer()
		start = realTime + self.firstBlock.get_size()

		if secondBlock.__class__ == RequestBlock:
			end = secondBlock.get_start()

			if end - start > 0:
				firstBlock = FreeBlock(start, end)
				firstBlock.set_left_block(None)
				firstBlock.set_right_block(secondBlock)
				secondBlock.set_left_block(firstBlock)

				self.firstBlock = firstBlock
			else:
				self.firstBlock = secondBlock
				secondBlock.set_left_block(None)
		else:
			secondBlock.set_start(start)
			secondBlock.set_left_block(None)

			self.firstBlock = secondBlock

		return requestBlock.get_request()

	def is_empty(self):
		return self.firstBlock == self.lastBlock

	def _update_first_block(self, removedBlock, newLeftBlock, newRequestBlock):
		if self.firstBlock != removedBlock:
			return

		if newLeftBlock != None:
			self.firstBlock = newLeftBlock
			return

		self.firstBlock = newRequestBlock

	def _update_last_block(self, removedBlock, newRightBlock, newRequestBlock):
		if self.lastBlock != removedBlock:
			return

		if newRightBlock != None:
			self.lastBlock = newRightBlock
			return

		self.lastBlock = newRequestBlock

	def _update_first_freeblock(self):
		if self.firstBlock.__class__ != FreeBlock:
			return

		realTime = Simulation.get_clock_pointer()
		if self.firstBlock.get_start() == realTime:
			return

		self.firstBlock.set_start(realTime)
		
		if self.firstBlock.get_size() <= 0:
			self.firstBlock.rightBlock.leftBlock = None
			self.firstBlock = self.firstBlock.rightBlock