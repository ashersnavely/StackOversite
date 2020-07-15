import ctypes
import threading


def wait_any(*args, parent_event=threading.Event()):
    daemons = [threading.Thread(target=__wait, args=(event, parent_event), daemon=True) for event in args]

    for thread in daemons:
        thread.start()

    parent_event.wait()

    for thread in daemons:
        if thread.is_alive():
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, ctypes.py_object(SystemExit))
        thread.join()


def __wait(event: threading.Event, parent_event: threading.Event):
    event.wait()
    parent_event.set()
