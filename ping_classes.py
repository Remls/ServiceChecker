from enum import Enum
import datetime
import re


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

class PingResponse:
    def __init__(self, service: Service, status: str, code: int, ping_time: int):
        self.service = service
        self.status = status
        self.code = code
        self.ping_time = ping_time

    def format_message(self, template: str):
        template = re.sub(r"\$TAG\$", self.service.tag.value, template)
        template = re.sub(r"\$SERVICE\$", self.service.name, template)
        template = re.sub(r"\$CODE\$", str(self.code), template)
        template = re.sub(r"\$PING\$", str(self.ping_time), template)
        return template

    def __str__(self) -> str:
        timestamp = str(datetime.datetime.now())
        return f"{timestamp} - {self.status} - {self.code} - p{self.ping_time}"
