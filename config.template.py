from service_class import Service, Tag


BOT_TOKEN = "112233:ABCDEF"
CHAT_ID = "-1001111111"
MESSAGE_FORMAT = {
    "up": "🟢 <code>[$TAG$]</code> $SERVICE$ is up ($CODE$)",
    "down": "🔴 <code>[$TAG$]</code> $SERVICE$ is down ($CODE$)",
}
SERVICES = {
    "service-1": Service("Service 1", Tag.API, "https://some.url"),
    "service-2": Service("Service 2", Tag.WEBAPP, "https://some.url"),
    "service-3": Service("Service 3", Tag.WEBSITE, "https://some.url"),
}