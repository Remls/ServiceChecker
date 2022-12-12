import os
import datetime
import pytz
import requests
from requests.exceptions import SSLError
from ping_classes import PingResponse
from file_functions import remove_logfile, check_last_status, log_status, get_message_ids, set_message_id
from config import SERVICES, TG_BOT_TOKEN, TG_CHAT_IDS, TG_MESSAGE_FORMAT, DISCORD_WEBHOOKS, DISCORD_MESSAGE_FORMAT, TIMEZONE


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

    text = ""
    for ping_response in ping_responses:
        template = TG_MESSAGE_FORMAT[ping_response.status]
        text += ping_response.format_message(template) + "\n\n"


    # Check if valid timezone
    tz = pytz.timezone(TIMEZONE)
    if not tz:
        print(f"Invalid timezone: {TIMEZONE}")
        return
    now = datetime.datetime.now(tz=tz)
    now = now.strftime("%d/%m/%Y %H:%M")
    text += f"<i>Last updated: {now}</i>"
    
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

if __name__ == '__main__':
    # Clean existing logs if asked
    clean_logs = False
    if len(os.sys.argv) > 1:
        arg = os.sys.argv[1].lower()
        clean_logs = arg == "--clean" or arg == "-c"
    if clean_logs:
        print("Cleaning existing logs ...")
        for service in SERVICES:
            remove_logfile(service)

    responses = []
    for service in SERVICES:
        ssl = True
        try:
            url = service.url
            print(f"Pinging {service.name} ({url}) ...")
            resp = requests.get(url)
        except SSLError as e:
            ssl = False
            print("- Unable to verify SSL certificate; retrying without verifying ...")
            resp = requests.get(url, verify=False)
        code = resp.status_code
        new_status = "up" if resp.ok else "down"
        ping_time = int(resp.elapsed.total_seconds() * 1000)
        if not ssl:
            new_status += "-nossl"
        ping_response = PingResponse(service, new_status, code, ping_time)
        responses.append(ping_response)
        last_status = check_last_status(service)
        log_status(ping_response)
        if last_status != new_status:
            print(f"- Status changed from {last_status} to {new_status}")
            send_telegram_message(ping_response)
            send_discord_message(ping_response)

    send_all_statuses_to_telegram(responses)
