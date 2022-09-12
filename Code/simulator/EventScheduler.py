class EventScheduler:
	def __init__(self):
		self.eventQueue = PriorityQueue()

	def push_event_list(self, eventList):
		if eventList == None:
			return

		for event in eventList:
			self.eventQueue.put(event)

	def get_next_event(self):
		return self.eventQueue.get()

	def is_empty(self):
		return self.eventQueue.empty()