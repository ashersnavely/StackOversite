from Controller.site_controller import SiteController

answer_filter = '!0Zk(K7XPmzcD5i0yn_ma1geTe'
question_filter = '!4(L6jMwWwA*(H)jKD'

url = 'stackoverflow'

SiteController.get_instance().create_site(url, key='1yfsxJa1AC*GlxN6RSemCQ((')

SiteController.get_instance().get_site(url).create_task('gib answers', 'code', endpoint='answers', filter=answer_filter,
                                                        sort='creation', order='desc', tagged='python')
SiteController.get_instance().get_site(url).create_task('gib questions', 'code', endpoint='questions',
                                                        filter=question_filter,
                                                        sort='creation', order='asc', tagged='python')

tasks = SiteController.get_instance().get_site(url).get_tasks()

for task_name in tasks:
    SiteController.get_instance().get_site(url).get_task(task_name).start()

input()
