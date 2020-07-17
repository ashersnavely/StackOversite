from json import JSONEncoder


class TaskStatus(object):
    def __init__(self, task):
        self.error = task.errored
        self.working = task.working
        self.page = task.page
        self.has_more = task.has_more
        self.total_avail = task.total
        self.processed = task.processed


class StatusEncoder(JSONEncoder):
    def default(self, o: TaskStatus):
        return o.__dict__
