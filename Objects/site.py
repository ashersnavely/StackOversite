from time import sleep

from stackapi import StackAPI

from Controller.site_constants import SetupMethods, rate_limit
from DTO.site_status import SiteStatus
from Objects.task import Task
from Utility.observable import Observable
from Utility.observer import Observer
from Utility.synchronization import Synchronize


class Site(StackAPI, Observable, Observer):
    def __init__(self, site: str, **kwargs):
        self.throttle = rate_limit

        StackAPI.__init__(self, site, max_pages=1, **kwargs)
        Observable.__init__(self)

        self.errored = set()
        self.working = set()
        self.finished = set()
        self.paused = set()

        self.tags = self.fetch(SetupMethods.Tags.value)['items']

        self.tasks = dict()

    @Synchronize
    def fetch(self, *args, **kwargs):
        sleep(self.throttle)
        return super().fetch(*args, **kwargs)

    def update(self, task: Task):
        if not task.working:
            if task in self.working:
                self.working.remove(task)

            if task.error:
                self.errored.add(task)
            elif not task.has_more:
                self.finished.add(task)
            else:
                self.paused.add(Task)
        if task.working:
            if task in self.paused:
                self.paused.remove(task)

            self.working.add(Task)

        self.notify()

    def get_tags(self):
        return self.tags

    def get_status(self):
        return SiteStatus(self)

    def get_tasks(self):
        return self.tasks

    def get_task(self, task_name: str):
        return self.tasks[task_name]

    def create_task(self, task_name: str, *args, **kwargs):
        task = Task(self, task_name, *args, **kwargs)
        task.subscribe(self)

        self.tasks.update({task_name: task})

    def delete_task(self, task_name: str):
        self.tasks.pop(task_name)
