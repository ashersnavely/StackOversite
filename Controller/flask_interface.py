from flask import Flask, jsonify

from Controller.site_constants import *
from Controller.site_controller import SiteController

app = Flask('StackExchangeScraper')


# TODO finish Flask restful api, review restful design
def run():
    app.run(debug=True)


@app.route('/')
def hello():
    return 'Landing Page o-o'


@app.route('/site_options', methods=['GET'])
def site_options():
    return jsonify({'site_options': SiteController.get_instance().site_options,
                    'cacheable': True})


# TODO update with DTO?
@app.route('/methods', methods=['GET'])
def methods():
    return jsonify({'methods': {method.value: submethods for method, submethods in
                                SiteController.get_instance().method_options.items()},
                    'cacheable': True})


@app.route('/fields', methods=['GET'])
def fields():
    return jsonify({'fields': [field.value for field in Fields],
                    'cacheable': True})


@app.route('/sorts', methods=['GET'])
def sorts():
    return jsonify({'sorts': [sort.value for sort in Sorts],
                    'cacheable': True})


@app.route('/orders', methods=['GET'])
def orders():
    return jsonify({'orders': [order.value for order in Orders],
                    'cacheable': True})


# TODO update with DTO?
@app.route('/tags/<path:site>', methods=['GET'])
def tags(site: str):
    return jsonify({'tags': SiteController.get_instance().get_tags(site),
                    'cacheable': True})


@app.route('/sites', methods=['GET'])
def sites():
    return jsonify({'sites': SiteController.get_instance().sites.keys(),
                    'cacheable': False})


# TODO figure out how to do optional or var args for the keys and such
@app.route('/sites/<path:site><string:key>', methods=['PUT'])
def site_create(site: str, key: str):
    SiteController.get_instance().create_site(site, key=key)


@app.route('/sites/<path:site>', methods=['DELETE'])
def site_delete(site: str):
    SiteController.get_instance().delete_site(site)


@app.route('/sites/<path:site>', methods=['GET'])
def site_status(site: str):
    return jsonify({'site': SiteController.get_instance().get_site(site).get_status()})


@app.route('/sites/<path:site>/tasks')
def tasks(site: str):
    return SiteController.get_instance().get_site(site).tasks.keys()


# TODO
def task_create(site: str, method: str, sort: str, order: str, tag: str, page: int,
                fromdate: int, todate: int, key: str):
    pass


# TODO remove task results from database as well
def task_delete(site: str, task: str):
    SiteController.get_instance().get_site(site).delete_task(task)


def task_start(site: str, task: str):
    SiteController.get_instance().get_site(site).get_task(task).start()


def task_pause(site: str, task: str):
    SiteController.get_instance().get_site(site).get_task(task).pause()


def task_resume(site: str, task: str):
    SiteController.get_instance().get_site(site).get_task(task).resume()


def task_status(site: str, task: str):
    SiteController.get_instance().get_site(site).get_task(task).get_status()


# TODO this will start a LARGE transfer.... need to check out some file transfer techniques?
def task_results():
    pass
