import random
import threading
from threading import Event, Condition
from time import sleep

from Utility.event_wait import wait_any


def random_event_set(event: Event):
    sleep(random.randrange(5))

    event.set()


def random_condition_set(condition: Condition):
    sleep(random.randrange(5))

    with condition:
        condition.notify_all()


event = Event()
condition = Condition()

threading.Thread(target=random_condition_set, args=(condition,), daemon=True).start()

wait_any(event, condition)

print('wooh')
