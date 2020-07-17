import threading
from queue import Queue

from bs4 import BeautifulSoup

from Controller.database_controller import DatabaseController
from Controller.site_constants import Fields
from DTO.post import PostTypes, Post
from DTO.task_status import TaskStatus
from Utility.observable import Observable
from Utility.thread_executioner import ThreadExecutioner


# TODO finalize DB dumping method
class Task(Observable):
    def __init__(self, site, name, *args, **kwargs):
        Observable.__init__(self)

        self.site = site
        self.name = name

        self.error = None
        self.working = False
        self.page = 1
        self.has_more = True
        self.total = 0
        self.processed = 0
        self.processed_lock = threading.Lock()

        self.post_queue = Queue()

        self.requester = ThreadExecutioner(self.request, None, **kwargs)
        self.scraper = ThreadExecutioner(self.scrape, self.post_queue, *args)

    def request(self, **kwargs):
        kwargs[Fields.page.value] = self.page

        try:
            status = self.site.fetch(**kwargs)
            response = status.pop('items')

            for item in response:
                self.post_queue.put(item)

            if not self.total and 'total' in status:
                self.total = status['total']

            if 'has_more' in status and status['has_more']:
                self.page += 1
            else:
                self.finish()

                self.has_more = False
                self.working = False
        except Exception as error:
            self.error = error
            print(error)
            self.working = False

            raise error
        finally:
            self.notify()

    def scrape(self, post, *args):
        post_id = None
        post_type = None
        for key in post:
            if 'id' in key:
                post_id = post[key]

                if PostTypes.Answer.value in key:
                    post_type = PostTypes.Answer
                elif PostTypes.Question.value in key:
                    post_type = PostTypes.Question
                else:
                    post_type = PostTypes.Comment

                break

        link = post['link']
        soup = BeautifulSoup(post['body'], "html.parser")

        tags = {}
        for tag in args:
            if not isinstance(tag, dict):
                for elem in soup.find_all(tag):
                    tags.update({tag: elem.text})

        tag_attrs = {}
        for arg in args:
            if isinstance(arg, dict):
                for tag, attr in arg.items():
                    for elem in soup.find_all(tag):
                        tags.update({tag: elem.attrs[attr]})

        data = {**tags, **tag_attrs}
        if data:
            DatabaseController.get_instance().dump(Post(post_id, data, link, post_type))

        with self.processed_lock:
            self.processed += 1

    def get_status(self):
        return TaskStatus(self)

    def start(self):
        self.scraper.start()
        self.requester.start()

        self.working = True
        self.notify()

    def pause(self):
        self.requester.pause()
        self.scraper.pause()

        self.working = False
        self.notify()

    def resume(self):
        self.requester.resume()
        self.scraper.resume()

        self.working = True
        self.notify()

    def finish(self):
        self.requester.stop()
        self.scraper.finish()

        self.working = False
        self.notify()

    def stop(self):
        self.requester.stop()
        self.scraper.stop()

        self.working = False
        self.notify()
