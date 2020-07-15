from enum import Enum

api_url = 'https://api.stackexchange.com'
api_version = '2.2'

rate_limit = 1 / 30


class SetupMethods(Enum):
    Tags = 'tags'
    Info = 'info'


class Methods(Enum):
    answers = 'answers'
    comments = 'comments'
    posts = 'posts'
    questions = 'questions'


class Sorts(Enum):
    activity = 'activity'
    votes = 'votes'
    creation = 'creation'
    relevance = 'relevance'
    hot = 'hot'
    week = 'week'
    month = 'month'


class Orders(Enum):
    descending = 'desc'
    ascending = 'asc'


class Fields(Enum):
    sort = 'sort'
    order = 'order'
    tag = 'tag'
    page = 'page'
    page_size = 'pagesize'
    from_date = 'fromdate'
    to_date = 'todate'
    max = 'max'
    min = 'min'
    key = 'key'
    backoff = 'backoff'
