import json, os

class LongTermMemory:
    def __init__(self, path="memory.json"):
        self.path = path
        if os.path.exists(path):
            self.data = json.load(open(path))
        else:
            self.data = []

    def add(self, item):
        self.data.append(item)
        json.dump(self.data, open(self.path, "w"), indent=2)
