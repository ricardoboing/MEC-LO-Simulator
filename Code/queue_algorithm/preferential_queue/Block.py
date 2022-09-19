class Block:
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.leftBlock = None
		self.rightBlock = None

	def get_start(self):
		return self.start

	def get_end(self):
		return self.end

	def get_size(self):
		return self.end - self.start

	def set_right_block(self, rightBlock):
		self.rightBlock = rightBlock

	def set_left_block(self, leftBlock):
		self.leftBlock = leftBlock

	def get_left_block(self):
		return self.leftBlock

	def get_right_block(self):
		return self.rightBlock