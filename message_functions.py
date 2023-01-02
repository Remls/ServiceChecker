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
    for chat in TG_CHAT_IDS:
        params = {
            "text": text,
            "parse_mode": "HTML",
            "disable_notification": silent
        }
        if isinstance(chat, dict):
            params["chat_id"] = chat["chat_id"]
            if "topic_id" in chat:
                params["message_thread_id"] = chat["topic_id"]
        else:
            params["chat_id"] = chat
        requests.get(
            f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
            params
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
    # 12 Dec 2022 14:00
    now = now.strftime("%d %b %Y, %H:%M")

    text = f"<u><b>ALL STATUSES</b></u>\n<i>Last updated {now}</i>\n\n"
    for ping_response in ping_responses:
        template = TG_MESSAGE_FORMAT[ping_response.status]
        text += ping_response.format_message(template) + "\n\n"
    
    message_ids = get_message_ids()
    for chat in TG_CHAT_IDS:
        chat_id = None
        topic_id = None
        if isinstance(chat, dict):
            chat_id = chat["chat_id"]
            if "topic_id" in chat:
                topic_id = chat["topic_id"]
        else:
            chat_id = chat
        msg_id = message_ids.get(chat_id)
        if msg_id:
            resp = edit_existing_all_status_message(text, chat_id, msg_id)
            # If the message was deleted, send a new one
            if not resp.ok:
                send_new_all_status_message(text, chat_id, topic_id)
        else:
            send_new_all_status_message(text, chat_id, topic_id)

def edit_existing_all_status_message(text, chat_id, message_id):
    """Edit existing All Statuses message on Telegram"""
    return requests.get(
        f"https://api.telegram.org/bot{TG_BOT_TOKEN}/editMessageText",
        params = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": "HTML"
        }
    )

def send_new_all_status_message(text, chat_id, topic_id = None):
    """Send new All Statuses message to Telegram"""
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if topic_id:
        params["message_thread_id"] = topic_id
    resp = requests.get(
        f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
        params
    )
    if resp.ok:
        msg_id = resp.json()["result"]["message_id"]
        set_message_id(chat_id, msg_id)
