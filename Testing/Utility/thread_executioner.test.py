import random
from string import ascii_letters
from time import sleep

from Utility.thread_executioner import *


def fooie(task: str, test=None):
    if test:
        print(test)
    print(f'{threading.current_thread().getName()} performing task {task}')


tasks = Queue()
for i in range(100000):
    foo = ''
    for n in range(10):
        foo += random.choice(ascii_letters)

    tasks.put(foo)

freddy = ThreadExecutioner(fooie, tasks, 'test')
jason = ThreadExecutioner(fooie, None, 'test')

for executioner in (freddy, jason):
    executioner.start()

    sleep(2)
    executioner.pause()
    sleep(5)

    executioner.resume()

    sleep(2)
    executioner.pause()
    sleep(5)

    executioner.stop()
