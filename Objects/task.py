from queue import Queue
from threading import Event

from Controller.site_constants import Fields
from DTO.task_status import TaskStatus
from Utility.event_wait import wait_any
from Utility.thread_executioner import ThreadExecutioner


# TODO add DB connection to dump data into
class Task(object):
    def __init__(self, site, name, **kwargs):
        self.site = site
        self.name = name
        self.status = TaskStatus()

        self.page = 1
        self.has_more = True
        self.post_queue = Queue()

        self.requester = ThreadExecutioner(self.request, None, **kwargs)
        self.scraper = ThreadExecutioner(self.scrape, self.post_queue, 'code')
        # self.watch_tower = ThreadExecutioner(self.monitor, None)

    # TODO notify on failure of task, use observer!
    def monitor(self):
        wait_any(self.requester.kill_switch, self.scraper.kill_switch, parent_event=Event())

    # TODO check if has_more
    def request(self, **kwargs):
        kwargs[Fields.page.value] = self.page

        status = self.site.fetch(**kwargs)
        response = status.pop('items')
        self.site.set_status(**status)

        self.page += 1

        for item in response:
            self.post_queue.put(item)

    # TODO actually process the post items to pull out specified html tagged items
    #  they will be part of args
    # noinspection PyMethodMayBeStatic
    def scrape(self, post, *args):
        print(post)
        pass

    def get_status(self):
        return self.status

    def start(self):
        self.scraper.start()
        self.requester.start()

    def pause(self):
        self.requester.pause()
        self.scraper.pause()

    def resume(self):
        self.requester.resume()
        self.scraper.resume()

    def stop(self):
        self.requester.stop()
        self.scraper.stop()
