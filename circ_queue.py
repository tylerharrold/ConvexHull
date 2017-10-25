import copy
def Hull_Queue:
    def __init__(self):
        self.queue = []
        self.head = 0
        self.upper_tick = -1
        self.lower_tick = -1

    # inserts a given element to the front of the queue
    def enqueue(self, addition):
        # check to see if first addition
        if self.is_empty():
            self.queue.append((addition,))
        else:
            self.queue.head.insert(0, (addition,)) 

    # returns the current head of the queue (the head is removed from the queue)
    def dequeue(self):
        if self.is_empty():
            return None
        else:
            return_node = self.queue.pop(0)[0]
            return self.queue.pop(0)[0]

    # returns true if queue is empty, false otherwise
    def is_empty(self):
        return not len(self.queue)

    # dumps the entire queue and returns a copy of the previous queue
    def dump_queue(self):
        return_copy = []
        for node in self.queue:
            return_copy.append(

        self.queue = []
        self.head = 0
        return return_copy

    # accepts a list and turns it into a queue
    def queueify(self , incoming_list):
        self.dump_queue()
        self.queue = copy.deepcopy(incoming_list)
        self.head = 0

    # returns the value of the position at head (in copy form)
    def peek_head(self):
        return (self.queue[head][0], self.queue[head][1])

    # returns copy of the value one rotation clockwise
    def peek_cw(self):
        self.rotate_cw()
        peek = self.peek_head()
        self.rotate_ccw()
        return peek

    # returns copy of the value one rotation counter clockwise
    def peek_ccw(self):
        self.rotate_ccw()
        peek = self.peek_head()
        self.rotate_cw()
        return peek

    # rotates the head of the queue clockwise
    def rotate_cw(self):
        self.head = (self.head + 1) % len(self.queue)

    # rotates the head of the queue counter clockwise
    def rotate_ccw(self):
        self.head = (self.head - 1) % len(self.queue)

    # marks upper tick
    def mark_upper(self):
        self.upper_tick = head

    # marks lower tick
    def mark_lower(self):
        self.lower_tick = head

    # eliminates items on the queue between upper and lower tick, clockwise (provided they both exist) and sets head to upper tick
    # wipes previou ticks
    def trim_cw(self):
        if self.upper_tick != -1 and self.lower_tick != -1:
            head = self.upper_tick
