import random
from string import ascii_letters
from time import sleep

from Utility.thread_executioner import *


def fooie(task: str, test=None):
    sleep(random.randrange(5))

    if test:
        print(test)
    print(f'{threading.current_thread().getName()} performing task {task}')


tasks = Queue()
freddy = ThreadExecutioner(fooie, tasks, 'test')

for i in range(100):
    foo = ''
    for n in range(10):
        foo += random.choice(ascii_letters)

    tasks.put(foo)

sleep(15)
freddy.kill_switch.set()

jason = ThreadExecutioner(fooie, None, 'test')
sleep(15)
