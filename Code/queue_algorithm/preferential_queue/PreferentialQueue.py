from simulator.Simulation import *
from queue_algorithm.preferential_queue.FreeBlock import *
from queue_algorithm.RequestQueue import *
import math

class PreferentialQueue(RequestQueue):
	def __init__(self):
		initialBlock = FreeBlock(0, math.inf)

		self.firstBlock = initialBlock
		self.lastBlock = initialBlock

	def push_request(self, request, force=False):
		self._update_first_freeblock()
		block = self.lastBlock

		while block != None:
			if block.__class__ == FreeBlock:
				leftBlock, requestBlock, rightBlock = block.alloc(request, False)

				if (leftBlock != None) or (requestBlock != None) or (rightBlock != None):
					self._update_first_block(block, leftBlock, requestBlock)
					self._update_last_block(block, rightBlock, requestBlock)
					return True

			block = block.get_left_block()

		if force:
			block = self.lastBlock
			leftBlock, requestBlock, rightBlock = block.alloc(request, force)
			self._update_first_block(block, leftBlock, requestBlock)
			self._update_last_block(block, rightBlock, requestBlock)

			return True
		return False

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
			self.rightBlock.leftBlock = None
			self.firstBlock = self.rightBlock