from json import JSONEncoder


class SiteStatus(object):
    def __init__(self, site):
        self.error = [task.name for task in site.errored]
        self.working = [task.name for task in site.working]
        self.finished = [task.name for task in site.finished]
        self.paused = [task.name for task in site.paused]


class StatusEncoder(JSONEncoder):
    def default(self, o: SiteStatus):
        return o.__dict__
