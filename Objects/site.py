import threading
from time import sleep

from stackapi import StackAPI

from Controller.site_constants import SetupMethods, rate_limit
from DTO.site_status import SiteStatus


class Site(StackAPI):
    def __init__(self, url: str, **kwargs):
        self.throttle = rate_limit
        self.throttle_lock = threading.Lock()

        super().__init__(url, max_pages=1, **kwargs)

        self.status = SiteStatus()
        self.tags = self.fetch(SetupMethods.Tags.value)['items']

        self.tasks = dict()

    def fetch(self, *args, **kwargs):
        with self.throttle_lock:
            sleep(self.throttle)
            return super().fetch(*args, **kwargs)

    def update_status(self):
        for name, scraper in self.tasks.items():
            # TODO
            pass

    def get_tags(self):
        return self.tags

    def get_status(self):
        return self.status

    def get_tasks(self):
        return self.tasks.keys()

    def init_task(self):
        # self.tasks.update({task_name: Task(task_name, self, **kwargs)})
        pass

    def delete_task(self):
        # TODO
        pass
