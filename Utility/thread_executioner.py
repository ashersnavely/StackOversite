import logging
import threading
from queue import Queue, Empty

from Utility.read_write_lock import RWLock, WriteLock, ReadLock


# TODO thread limit... ?
class ThreadExecutioner:
    _timeout = 1

    @staticmethod
    def __kill(victim: threading.Thread):
        was_alive = victim.is_alive()
        victim.join()
        return was_alive

    def __init__(self, target, tasks: Queue, *args, **kwargs):
        self._started = False
        self._error = None

        self.failure = threading.Event()
        self.kill_switch = threading.Event()
        self._run = threading.Event()

        if not tasks:
            self.thread = threading.Thread(target=ThreadExecutioner.__solitary, args=(self, target, *args),
                                           kwargs=kwargs, daemon=True)
            self.thread.setName(f'Solitary Confinement id#{threading.current_thread().ident}')
        else:
            self.finished = Queue()

            self.worker_count = 0
            self.worker_lock = RWLock()

            self.thread = threading.Thread(target=ThreadExecutioner.__spawn, args=(self, target, tasks, *args),
                                           kwargs=kwargs, daemon=True)
            self.thread.setName(f'Work Camp id#{threading.current_thread().ident}')

    def __del__(self):
        self.stop()

    def get_error(self):
        return self._error

    def start(self):
        if not self._started:
            self._run.set()
            self.thread.start()

    def pause(self):
        self._run.clear()

    def resume(self):
        self._run.set()

    def stop(self):
        self.kill_switch.set()
        self._run.set()

        self.thread.join()

    def __fail(self, error):
        self.stop()

        self._error = error
        self.failure.set()

    def __solitary(self, target, *args, **kwargs):
        while True:
            try:
                target(*args, **kwargs)
            except Exception as oop:
                self.__fail(oop)
            finally:
                if not self._run.is_set():
                    self._run.wait()
                if self.kill_switch.is_set():
                    return

    def __spawn(self, target, tasks: Queue, *args, **kwargs):
        current_thread_name = threading.current_thread().getName()

        thread_killer = threading.Thread(target=ThreadExecutioner.__executioner, args=(self, ThreadExecutioner.__kill))
        thread_killer.setName(f'{current_thread_name}\'s Thread Killer')

        logging.info(f'Spawning new executioner, {thread_killer.getName()}.')
        thread_killer.start()

        while True:
            try:
                task = tasks.get(timeout=ThreadExecutioner._timeout)
                worker = threading.Thread(target=ThreadExecutioner.__work_camp, args=(self, target, task, *args),
                                          kwargs=kwargs)
                worker.setName(f'{current_thread_name}\'s Worker id#{self.worker_count}')

                with WriteLock(self.worker_lock):
                    if not self.kill_switch.is_set():
                        logging.info(f'Spawning new worker, {worker.getName()} for task {task}.')

                        self.worker_count += 1
                        worker.start()
                    else:
                        tasks.put(task)
            except Empty:
                pass
            finally:
                if not self._run.is_set():
                    self._run.wait()
                if self.kill_switch.is_set():
                    ThreadExecutioner.__kill(thread_killer)
                    return

    def __work_camp(self, target, *args, **kwargs):
        try:
            target(*args, **kwargs)
        except Exception as oop:
            self.__fail(oop)
        finally:
            self.finished.put(threading.current_thread())

    def __executioner(self, kill_method):
        while True:
            try:
                kill_method(self.finished.get(timeout=ThreadExecutioner._timeout))
                self.finished.task_done()

                with WriteLock(self.worker_lock):
                    self.worker_count -= 1
            except Empty:
                if not self._run.is_set():
                    self._run.wait()
            finally:
                if self.kill_switch.is_set():
                    with ReadLock(self.worker_lock):
                        if not self.worker_count:
                            return
