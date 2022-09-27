from queue_algorithm.preferential_queue.PreferentialQueue import *
from distributor.OriginalSequentialForwarding import *

class ProposedDistributor(OriginalSequentialForwarding):
	QueueClass = PreferentialQueue