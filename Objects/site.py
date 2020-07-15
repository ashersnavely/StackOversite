import threading
from time import sleep

from stackapi import StackAPI

from Controller.site_constants import SetupMethods, rate_limit
from DTO.site_status import SiteStatus
from Objects.task import Task


class Site(StackAPI):
    def __init__(self, site: str, **kwargs):
        self.throttle = rate_limit
        self.throttle_lock = threading.Lock()

        super().__init__(site, max_pages=1, **kwargs)

        self.status = SiteStatus()
        self.tags = self.fetch(SetupMethods.Tags.value)['items']

        self.tasks = dict()

    def fetch(self, *args, **kwargs):
        with self.throttle_lock:
            sleep(self.throttle)
            return super().fetch(*args, **kwargs)

    # TODO
    def update_status(self):
        pass

    def get_tags(self):
        return self.tags

    def get_status(self):
        return self.status

    def get_task(self, task_name: str):
        return self.tasks[task_name]

    def create_task(self, task_name: str, **kwargs):
        self.tasks.update({task_name: Task(task_name, self, **kwargs)})

    def delete_task(self, task_name: str):
        self.tasks.pop(task_name)
