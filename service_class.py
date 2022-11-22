from enum import Enum


class Tag(Enum):
    API = 'api'
    WEBAPP = 'webapp'
    WEBSITE = 'website'

class Service:
    def __init__(self, name: str, tag: Tag, url: str):
        self.name = name
        self.tag = tag
        self.url = url