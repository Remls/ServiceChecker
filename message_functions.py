import datetime
import requests
import pytz
from file_functions import get_message_ids, set_message_id
from ping_classes import PingResponse
from config import TG_BOT_TOKEN, TG_CHAT_IDS, TG_MESSAGE_FORMAT, DISCORD_WEBHOOKS, DISCORD_MESSAGE_FORMAT, TIMEZONE


def send_telegram_message(ping_response: PingResponse, silent = False):
    if not TG_BOT_TOKEN or not TG_CHAT_IDS:
        print("Telegram is not configured; skipping ...")
        return

    template = TG_MESSAGE_FORMAT[ping_response.status]
    text = ping_response.format_message(template)
    for chat_id in TG_CHAT_IDS:
        requests.get(
            f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
            params = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_notification": silent
            }
        )

def send_discord_message(ping_response: PingResponse):
    if not DISCORD_WEBHOOKS:
        print("Discord is not configured; skipping ...")
        return

    template = DISCORD_MESSAGE_FORMAT[ping_response.status]
    text = ping_response.format_message(template)
    for webhook_url in DISCORD_WEBHOOKS:
        requests.post(
            webhook_url,
            json = {
                "content": text,
            }
        )

def send_all_statuses_to_telegram(ping_responses: list):
    if not TG_BOT_TOKEN or not TG_CHAT_IDS:
        print("Telegram is not configured; skipping ...")
        return

    if not ping_responses:
        return

    # Check if valid timezone
    tz = pytz.timezone(TIMEZONE)
    if not tz:
        print(f"Invalid timezone: {TIMEZONE}")
        return
    now = datetime.datetime.now(tz=tz)
    # 12 Dec 2022 12:00
    now = now.strftime("%d %b %Y, %H:%M")

    text = f"<u><b>ALL STATUSES</b></u>\n<i>Last updated {now}</i>\n\n"
    for ping_response in ping_responses:
        template = TG_MESSAGE_FORMAT[ping_response.status]
        text += ping_response.format_message(template) + "\n\n"
    
    message_ids = get_message_ids()
    for chat_id in TG_CHAT_IDS:
        msg_id = message_ids.get(chat_id)
        if msg_id:
            resp = edit_existing_message(chat_id, msg_id, text)
            # If the message was deleted, send a new one
            if not resp.ok:
                send_new_message(chat_id, text)
        else:
            send_new_message(chat_id, text)

def edit_existing_message(chat_id, message_id, text):
    return requests.get(
        f"https://api.telegram.org/bot{TG_BOT_TOKEN}/editMessageText",
        params = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": "HTML"
        }
    )

def send_new_message(chat_id, text):
    resp = requests.get(
        f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
        params = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
    )
    if resp.ok:
        msg_id = resp.json()["result"]["message_id"]
        set_message_id(chat_id, msg_id)
