import queue

class MessageAnnouncer:
    '''
    Object used to manage a set of client stream queues.
    Call announce(msg) to post a message for distribution to all clients.
    Call listen() as a client to get access to the corresponding event queue.
    '''
    def __init__(self):
        self.listeners = []

    def listen(self):
        '''Register a client and receive the returned queue.
        '''
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        '''Distribute the msg passed in to all registered clients.'''
        for i in reversed(range(len(self.listeners))):
            try:
                print(f'Send {msg!r} to {self.listeners[i]!r}')
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]
