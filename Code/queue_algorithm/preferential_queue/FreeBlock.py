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
	if block != None:
		block.set_left_block(leftBlock)

	if leftBlock != None:
		leftBlock.set_right_block(block)

def _set_right_block(block, rightBlock):
	if block != None:
		block.set_right_block(rightBlock)

	if rightBlock != None:
		rightBlock.set_left_block(block)

def get_request_size(request):
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

def has_space(block, area, request):
	if area <= 0:
		return True

	if block == None:
		return False

	if block.__class__ != RequestBlock:
		areaUtil = _get_useful_area(block, request)
		area -= areaUtil["size"]

	return has_space(block.leftBlock, area, request)

def shift_left(block, steps):
	if steps <= 0:
		return

	if block.__class__ == RequestBlock:
		block.end -= steps
		block.start -= steps
	else:
		steps -= block.get_size()

		if steps < 0:
			blockSize = (-1) * steps
			block.end = block.start + blockSize
			return

		_set_left_block(block.rightBlock, block.leftBlock)

	shift_left(block.leftBlock, steps)

def get_last_util_block(block, request):
	while block != None:
		if block.__class__ != RequestBlock:
			areaUtil = _get_useful_area(block, request)

			if areaUtil["size"] > 0:
				return block

		block = block.leftBlock
	return None

def get_first_block(block):
	if block.leftBlock == None:
		return block

	return get_first_block(block.leftBlock)

class FreeBlock(Block):
	def __init__(self, start, end):
		super().__init__(start, end)

	def set_start(self, start):
		self.start = start

	def alloc(self, request, forcedPush=False):
		usefulArea = _get_useful_area(self, request)
		requestSize = get_request_size(request)

		if usefulArea["size"] == 0 or (usefulArea["size"] < requestSize and forcedPush):
			shiftArea = 0
			usefulArea["start"] = self.get_start()
			usefulArea["end"] = self.get_start() + requestSize
			usefulArea["size"] = requestSize
		else:
			shiftArea = requestSize - usefulArea["size"]
			usefulArea["size"] = requestSize
			usefulArea["start"] = usefulArea["end"] - requestSize

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

		return rightBlock, shiftArea

	def split_block(self, start, end):
		blockStart = self.get_start()
		blockEnd = self.get_end()

		leftBlock = FreeBlock(blockStart, start)
		rightBlock = FreeBlock(end, blockEnd)

		if leftBlock.get_size() <= 0:
			leftBlock = None

		if rightBlock.get_size() <= 0:
			rightBlock = None

		return leftBlock, rightBlock