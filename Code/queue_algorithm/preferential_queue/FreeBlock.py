from queue_algorithm.preferential_queue.Block import *
from queue_algorithm.preferential_queue.RequestBlock import *

def _get_useful_area(block, request):
	blockStart = block.get_start()
	blockEnd = block.get_end()

	requestStart, requestEnd = _get_request_parameters(request)

	start = blockStart
	end = min(blockEnd, requestEnd)

	if start > end:
		start = 0
		end = 0

	return {
		"start": start,
		"end": end,
		"size": end - start
	}

def _set_left_block(block, leftBlock):
	block.set_left_block(leftBlock)

	if leftBlock != None:
		leftBlock.set_right_block(block)

def _set_right_block(block, rightBlock):
	block.set_right_block(rightBlock)

	if rightBlock != None:
		rightBlock.set_left_block(block)

def _get_request_size(request):
	service = request.get_service()
	return service.get_max_process_time()

def _get_request_parameters(request):
	service = request.get_service()
	serviceDeadline = service.get_deadline()

	serviceMaxProcessTime = service.get_max_process_time()
	requestGenerated = request.get_generated_time()

	requestMaxEnd = requestGenerated + serviceDeadline
	requestMaxStart = requestMaxEnd - serviceMaxProcessTime

	return requestMaxStart, requestMaxEnd

def _create_request_block(usefulArea, requestSize, request):
	requestStart = usefulArea["end"] - requestSize
	requestEnd = usefulArea["end"]

	return RequestBlock(requestStart, requestEnd, request)

class FreeBlock(Block):
	def __init__(self, start, end):
		super().__init__(start, end)

	def set_start(self, start):
		self.start = start

	def alloc(self, request):
		usefulArea = _get_useful_area(self, request)
		requestSize = _get_request_size(request)

		if usefulArea["size"] < requestSize:
			return None, None, None

		requestBlock = _create_request_block(usefulArea, requestSize, request)
		leftBlock, rightBlock = self.split_block(requestBlock.get_start(), requestBlock.get_end())

		if leftBlock != None:
			_set_left_block(leftBlock, self.leftBlock)
			_set_left_block(requestBlock, leftBlock)
		else:
			_set_left_block(requestBlock, self.leftBlock)

		if rightBlock != None:
			_set_right_block(rightBlock, self.rightBlock)
			_set_right_block(requestBlock, rightBlock)
		else:
			_set_right_block(requestBlock, self.rightBlock)

		return leftBlock, requestBlock, rightBlock

	def split_block(self, start, end):
		blockStart = self.get_start()
		blockEnd = self.get_end()

		leftBlock = FreeBlock(blockStart, start)
		rightBlock = FreeBlock(end, blockEnd)

		if leftBlock.get_size() == 0:
			leftBlock = None

		if rightBlock.get_size() == 0:
			rightBlock = None

		return leftBlock, rightBlock