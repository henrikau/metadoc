def _singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@_singleton
class UniqueID(object):
    def __init__(self):
        self.last_id = 0
    def get_id(self):
        self.last_id = self.last_id + 1
        return "%i" % self.last_id
