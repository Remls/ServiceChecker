from enum import Enum


class Tag(Enum):
    API = 'api'
    WEBAPP = 'webapp'
    WEBSITE = 'website'

class Service:
    def guess_key(name: str, tag: Tag):
        # If name ends in " API" or " App", remove it
        if name.endswith(' API'):
            name = name[:-4]
        elif name.endswith(' App'):
            name = name[:-4]

        # Remove parentheses and spaces
        key = name.lower().replace('(', '').replace(')', '').replace(' ', '-')

        # Add API tag to key
        if tag == Tag.API:
            key += '-api'

        return key


    def __init__(self, name: str, tag: Tag, url: str, key: str = None):
        self.name = name
        self.tag = tag
        self.url = url

        if key is None:
            key = Service.guess_key(name, tag)
        self.key = key