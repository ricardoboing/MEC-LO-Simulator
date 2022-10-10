class RequestPackage:
	def __init__(self, request, destination, forwardCounter=0):
		self.forwardCounter = forwardCounter
		self.request = request
		self.destination = destination

		self.previousDestinationList = [destination]

	def increment_forward_counter(self):
		self.forwardCounter += 1

	def set_new_destination(self, destination):
		self.previousDestinationList.append(self.destination)
		self.destination = destination

	def get_previous_destination_list(self):
		return self.previousDestinationList

	def get_destination(self):
		return self.destination

	def get_request(self):
		return self.request

	def get_forward_counter(self):
		return self.forwardCounter