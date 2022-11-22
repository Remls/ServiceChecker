from service_class import Service, Tag


BOT_TOKEN = "112233:ABCDEF"
CHAT_ID = "-1001111111"
MESSAGE_FORMAT = {
    "up": "🟢 <code>[$TAG$]</code> $SERVICE$ is up ($CODE$)",
    "down": "🔴 <code>[$TAG$]</code> $SERVICE$ is down ($CODE$)",
    "up-nossl": "🟢 <code>[$TAG$]</code> $SERVICE$ is up ($CODE$)\n⚠️ Failed to verify SSL certificate",
    "down-nossl": "🔴 <code>[$TAG$]</code> $SERVICE$ is down ($CODE$)\n⚠️ Failed to verify SSL certificate",
}
SERVICES = {
    "service-1": Service("Service 1", Tag.API, "https://some.url"),
    "service-2": Service("Service 2", Tag.WEBAPP, "https://some.url"),
    "service-3": Service("Service 3", Tag.WEBSITE, "https://some.url"),
}