from service_class import Service, Tag


# Telegram
# Leave TG_BOT_TOKEN and TG_CHAT_ID empty if you don't want to use Telegram
TG_BOT_TOKEN = "112233:ABCDEF"
TG_CHAT_ID = "-1001111111"
TG_MESSAGE_FORMAT = {
    "up": "🟢 <code>[$TAG$]</code> $SERVICE$ is up ($CODE$)",
    "down": "🔴 <code>[$TAG$]</code> $SERVICE$ is down ($CODE$)",
    "up-nossl": "🟢 <code>[$TAG$]</code> $SERVICE$ is up ($CODE$)\n    ⚠️ Failed to verify SSL certificate",
    "down-nossl": "🔴 <code>[$TAG$]</code> $SERVICE$ is down ($CODE$)\n    ⚠️ Failed to verify SSL certificate",
}

# Discord
# Leave DISCORD_WEBHOOK_URL empty if you don't want to use Discord
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz"
DISCORD_MESSAGE_FORMAT = {
    "up": "🟢 `[$TAG$]` $SERVICE$ is up ($CODE$)",
    "down": "🔴 `[$TAG$]` $SERVICE$ is down ($CODE$)",
    "up-nossl": "🟢 `[$TAG$]` $SERVICE$ is up ($CODE$)\n    ⚠️ Failed to verify SSL certificate",
    "down-nossl": "🔴 `[$TAG$]` $SERVICE$ is down ($CODE$)\n    ⚠️ Failed to verify SSL certificate",
}

SERVICES = {
    "service-1": Service("Service 1", Tag.API, "https://some.url"),
    "service-2": Service("Service 2", Tag.WEBAPP, "https://some.url"),
    "service-3": Service("Service 3", Tag.WEBSITE, "https://some.url", "some-custom-key"),
}