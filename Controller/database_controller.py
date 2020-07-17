import json
from datetime import datetime

from DTO.post import Post
from Utility.synchronization import Synchronize


# TODO implement NOSQL DB and setup this controller
class DatabaseController:
    _database_controller = None

    @staticmethod
    def get_instance():
        if not DatabaseController._database_controller:
            DatabaseController._database_controller = _DatabaseController()

        return DatabaseController._database_controller


class _DatabaseController:
    def __init__(self):
        self.file = open(f'scrape.{datetime.now()}.json', 'w')

    def __del__(self):
        self.file.close()

    @Synchronize
    def dump(self, post: Post):
        json.dump(post.__dict__, self.file)
