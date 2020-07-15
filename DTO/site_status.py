from json import JSONEncoder


class SiteStatus(object):
    def __init__(self, error=False, working_count=0, finished_count=0, paused_count=0):
        self.error = error
        self.working_count = working_count
        self.finished_count = finished_count
        self.paused_count = paused_count


class StatusEncoder(JSONEncoder):
    def default(self, o: SiteStatus):
        return o.__dict__
