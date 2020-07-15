from flask import Flask, jsonify

from Controller.site_constants import *
from Controller.site_controller import SiteController

app = Flask('StackExchangeScraper')


def run():
    app.run(debug=True)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/site_options', methods=['GET'])
def site_options():
    return jsonify({'site_options': SiteController.get_instance().site_options,
                    'cacheable': True})


@app.route('/methods', methods=['GET'])
def methods():
    # TODO update with DTO?
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


@app.route('/tags/<path:site>', methods=['GET'])
def tags(site: str):
    # TODO update with DTO?
    return jsonify({'tags': SiteController.get_instance().get_tags(site),
                    'cacheable': True})


def sites():
    # TODO
    pass


def site_init():
    # TODO
    pass


def site_delet():
    # TODO
    pass


@app.route('/site_status/<path:site>', methods=['GET'])
def site_status(site: str):
    # TODO
    # return jsonify({'status': json.dumps(SiteController.get_instance().get_status(site), cls=StatusEncoder),
    #                     'cacheable': False})
    pass


def tasks():
    # TODO
    pass


@app.route('/task_start/<path:site><string:method><string:sort><string:order><string:tag>'
           '<int:page><int:fromdate><int:todate><string:key>', methods=['PUT'])
def task_start(site: str, method: str, sort: str, order: str, tag: str, page: int,
               fromdate: int, todate: int, key: str):
    # TODO
    pass


def task_stop():
    # TODO
    pass


def task_resume():
    # TODO
    pass


def task_delete():
    # TODO
    # will remove task results from database as well
    pass


def task_status():
    # TODO
    pass


def task_results():
    # TODO
    # this will start a LARGE transfer.... need to check out some file transfer techniques?
    pass
