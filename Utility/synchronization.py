import threading
from functools import partial

"""Synchronization decorator, like Java's Synchronized annotation
    Keep in mind this is static and bound to class or a provided name, not bound to instance"""


def SynchronizeTo(name):
    return _SynchronizeTo(name).set_function


class _SynchronizeTo(object):
    __synchros__ = {}

    def __init__(self, name):
        if name not in _SynchronizeTo.__synchros__:
            _SynchronizeTo.__synchros__.update({name: threading.Lock()})

        self.name = name
        self.function = None

    def set_function(self, function):
        self.function = function

        return self

    def __get__(self, instance, owner):
        return partial(self.__call__, instance)

    def __call__(self, *args, **kwargs):
        _SynchronizeTo.__synchros__[self.name].acquire()
        try:
            return self.function(*args, **kwargs)
        finally:
            _SynchronizeTo.__synchros__[self.name].release()


class Synchronize(object):
    def __init__(self, function):
        self.lock = threading.Lock()
        self.function = function

    def __get__(self, instance, owner):
        return partial(self.__call__, instance)

    def __call__(self, *args, **kwargs):
        self.lock.acquire()
        try:
            return self.function(*args, **kwargs)
        finally:
            self.lock.release()
