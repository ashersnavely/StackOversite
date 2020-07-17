from enum import Enum
from json import JSONEncoder


class PostTypes(Enum):
    Answer = 'answer'
    Question = 'question'
    Comment = 'comment'


class Post(object):
    def __init__(self, post_id: int, data: str, link: str, post_type: PostTypes):
        self.id = post_id
        self.data = data
        self.link = link
        self.type = post_type.value


class PostEncoder(JSONEncoder):
    def default(self, post: Post):
        return post.__dict__
