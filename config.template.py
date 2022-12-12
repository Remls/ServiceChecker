from service_class import Service, Tag


# Telegram
# Leave TG_BOT_TOKEN and TG_CHAT_IDS empty if you don't want to use Telegram
TG_BOT_TOKEN = "112233:ABCDEF"
TG_CHAT_IDS = [
    "-1001111111",
]
TG_MESSAGE_FORMAT = {
    "up": "🟢 <code>[$TAG$]</code> $SERVICE$ is up (code $CODE$, $PING$ms)",
    "down": "🔴 <code>[$TAG$]</code> $SERVICE$ is down (code $CODE$, $PING$ms)",
    "up-nossl": "🟢 <code>[$TAG$]</code> $SERVICE$ is up (code $CODE$, $PING$ms)\n    ⚠️ Failed to verify SSL certificate",
    "down-nossl": "🔴 <code>[$TAG$]</code> $SERVICE$ is down (code $CODE$, $PING$ms)\n    ⚠️ Failed to verify SSL certificate",
}

# Discord
# Leave DISCORD_WEBHOOKS empty if you don't want to use Discord
DISCORD_WEBHOOKS = [
    "https://discordapp.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz",
]
DISCORD_MESSAGE_FORMAT = {
    "up": "🟢 `[$TAG$]` $SERVICE$ is up (code $CODE$, $PING$ms)",
    "down": "🔴 `[$TAG$]` $SERVICE$ is down (code $CODE$, $PING$ms)",
    "up-nossl": "🟢 `[$TAG$]` $SERVICE$ is up (code $CODE$, $PING$ms)\n    ⚠️ Failed to verify SSL certificate",
    "down-nossl": "🔴 `[$TAG$]` $SERVICE$ is down (code $CODE$, $PING$ms)\n    ⚠️ Failed to verify SSL certificate",
}

SERVICES = {
    "service-1": Service("Service 1", Tag.API, "https://some.url"),
    "service-2": Service("Service 2", Tag.WEBAPP, "https://some.url"),
    "service-3": Service("Service 3", Tag.WEBSITE, "https://some.url", "some-custom-key"),
}