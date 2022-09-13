from queue import PriorityQueue

class EventScheduler:
	_eventCounter = 0
	def __init__(self):
		self.eventQueue = PriorityQueue()
		self.eventDick = {}

	def _get_new_event_counter(self):
		eventCounter = str(EventScheduler._eventCounter)
		EventScheduler._eventCounter += 1

		return eventCounter

	def push_event(self, event):
		eventKey = str( self._get_new_event_counter() )

		temporalMoment = event.get_temporal_moment()
		self.eventDick[eventKey] = event

		self.eventQueue.put((temporalMoment, eventKey))

	def push_event_list(self, eventList):
		if eventList == None:
			return

		for event in eventList:
			self.push_event(event)

	def get_next_event(self):
		temporalMoment, eventKey = self.eventQueue.get()
		event = self.eventDick.pop(eventKey)

		return event

	def is_empty(self):
		return self.eventQueue.empty()