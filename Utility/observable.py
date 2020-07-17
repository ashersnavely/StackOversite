import threading

from Utility.observer import Observer


class Observable(object):
    def __init__(self):
        self.subscribers = set()
        self.hash = None

        self.subscriber_lock = threading.Lock()
        self.notification_lock = threading.Lock()

    def subscribe(self, observer: Observer):
        with self.subscriber_lock:
            self.subscribers.add(observer)

    def unsubscribe(self, observer: Observer):
        with self.subscriber_lock:
            self.subscribers.remove(observer)

    def notify(self):
        with self.notification_lock:
            new_hash = self.__hash__()

            if new_hash != self.hash:
                for subscriber in self.subscribers:
                    subscriber.update(self)

            self.hash = new_hash
