from queue import Queue
from threading import Event

from Controller.site_constants import Fields
from DTO.task_status import TaskStatus
from Utility.event_wait import wait_any
from Utility.thread_executioner import ThreadExecutioner


# TODO add DB connection to dump data into
# TODO seperate creation from thread starting
class Task(object):
    def __init__(self, name, site, **kwargs):
        self.name = name
        self.site = site
        self.status = TaskStatus()

        self.page = 1
        self.post_queue = Queue()

        self.requester = ThreadExecutioner(self.request, None, **kwargs)
        self.scraper = ThreadExecutioner(self.scrape, self.post_queue, 'code')

        self.error = Event()
        self.watch_tower = ThreadExecutioner(self.monitor, None)

    def monitor(self):
        wait_any(self.requester.kill_switch, self.scraper.kill_switch, parent_event=self.error)

        if self.requester.kill_switch.is_set():
            self.site.update_status()

            self.status.error = self.requester.err
            self.status.alive = self.requester.thread.is_alive()

        else:
            pass

    def request(self, **kwargs):
        kwargs[Fields.page.value] = self.page

        status = self.site.fetch(**kwargs)
        response = status.pop('items')
        self.site.set_status(**status)

        self.page += 1

        for item in response:
            self.post_queue.put(item)

    def scrape(self, post, *args):
        # TODO actually process the post items to pull out specified html tagged items
        #  they will be part of args
        print(post)
        pass

    def start_task(self, task_name: str, **kwargs):
        # TODO handle resuming a previously stopped task
        pass

    def stop(self, task_name: str, **kwargs):
        # TODO
        pass
