import atexit
import threading
from time import sleep

from Controller.database_controller import DatabaseController
from Controller.site_controller import SiteController


# For dev only!
def user_input():
    while True:
        sleep(1)

        i = input()
        if i == 'stop':
            for task_name in tasks:
                SiteController.get_instance().get_site(url).get_task(task_name).stop()
            break
        elif i == 'pause':
            for task_name in tasks:
                SiteController.get_instance().get_site(url).get_task(task_name).pause()
        elif i == 'resume':
            for task_name in tasks:
                SiteController.get_instance().get_site(url).get_task(task_name).resume()


def cleanup():
    DatabaseController.get_instance().persist()


answer_filter = '!0Zk(K7XPmzcD5i0yn_ma1geTe'
question_filter = '!4(L6jMwWwA*(H)jKD'

key = '1yfsxJa1AC*GlxN6RSemCQ(('

url = 'stackoverflow'

SiteController.get_instance().create_site(url, key=key)

SiteController.get_instance().get_site(url).create_task('gib answers', 'code', endpoint='answers', filter=answer_filter,
                                                        sort='creation', order='desc', tagged='python')
SiteController.get_instance().get_site(url).create_task('gib questions', {'a': 'href'}, endpoint='questions',
                                                        filter=question_filter,
                                                        sort='votes', order='asc', tagged='java')

tasks = SiteController.get_instance().get_site(url).get_tasks()
for task_name in tasks:
    SiteController.get_instance().get_site(url).get_task(task_name).start()

threading.Thread(target=user_input, daemon=True).start()
atexit.register(cleanup)
