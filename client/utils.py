def _singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@_singleton
class UniqueID(object):
    """ Singleton class to create unique IDs. """
    def __init__(self):
        """ Starts the ID counter at 0. """
        self.last_id = 0
    def get_id(self):
        """ Increments the ID counter and returns it. """
        self.last_id = self.last_id + 1
        return "%i" % self.last_id
