# memory/session.py
from collections import deque

class SessionMemory:
    def __init__(self, maxlen=200):
        self.history = deque(maxlen=maxlen)

    def append(self, item: dict):
        self.history.append(item)

    def last(self, n=5):
        return list(self.history)[-n:]

    def all(self):
        return list(self.history)
