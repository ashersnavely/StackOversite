from json import JSONEncoder


class TaskStatus(object):
    def __init__(self, error=None, alive=True, page=1, processed=0, has_more=False, total=0):
        self.error = error
        self.alive = alive
        self.page = page
        self.processed = processed
        self.has_more = has_more
        self.total = total


class StatusEncoder(JSONEncoder):
    def default(self, o: TaskStatus):
        return o.__dict__
