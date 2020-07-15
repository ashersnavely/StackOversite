from enum import Enum


class PostTypes(Enum):
    Answer = 'answer'
    Question = 'question'
    Comment = 'comment'


class Post(object):
    def __init__(self, post_id: int, snippet: str, link: str, post_type: PostTypes):
        self.id = post_id
        self.snippet = snippet
        self.link = link
        self.type = post_type.value
