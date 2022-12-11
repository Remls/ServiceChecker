import requests
from requests.exceptions import SSLError
import re
import os
import datetime
from config import SERVICES, TG_BOT_TOKEN, TG_CHAT_ID, TG_MESSAGE_FORMAT, DISCORD_WEBHOOK_URL, DISCORD_MESSAGE_FORMAT


def send_telegram_message(service_key: str, new_status = 'up', code = 200, silent = False):
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        print("Telegram is not configured; skipping ...")
        return

    service = SERVICES[service_key]
    text = TG_MESSAGE_FORMAT[new_status]
    text = re.sub(r"\$TAG\$", service.tag.value, text)
    text = re.sub(r"\$SERVICE\$", service.name, text)
    text = re.sub(r"\$CODE\$", str(code), text)
    requests.get(
        f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
        params = {
            "chat_id": TG_CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_notification": silent
        }
    )

def send_discord_message(service_key: str, new_status = 'up', code = 200, silent = False):
    if not DISCORD_WEBHOOK_URL:
        print("Discord is not configured; skipping ...")
        return

    service = SERVICES[service_key]
    text = DISCORD_MESSAGE_FORMAT[new_status]
    text = re.sub(r"\$TAG\$", service.tag.value, text)
    text = re.sub(r"\$SERVICE\$", service.name, text)
    text = re.sub(r"\$CODE\$", str(code), text)
    requests.post(
        DISCORD_WEBHOOK_URL,
        json = {
            "content": text,
        }
    )

def get_logfile_name(service_key: str):
    return f"logs/{service_key}.log"

def remove_logfile(service_key: str):
    log = get_logfile_name(service_key)
    if os.path.exists(log):
        os.remove(log)

def check_last_status(service_key: str):
    log = get_logfile_name(service_key)
    if not os.path.exists(log):
        return None
    with open(log) as f:
        lines = f.readlines()
        if not lines:
            return None
        lines.reverse()
        for l in lines:
            if l:
                return l.split(' - ')[1].strip()
    return None

def log_status(service_key: str, new_status = 'up', code = 200):
    log = get_logfile_name(service_key)
    timestamp = str(datetime.datetime.now())
    with open(log, 'a') as f:
        f.write(f"{timestamp} - {new_status} - {code}\n")


if __name__ == '__main__':
    # Clean existing logs if asked
    clean_logs = False
    if len(os.sys.argv) > 1:
        clean_logs = os.sys.argv[1] == "--clean" or os.sys.argv[1] == "-c"
    if clean_logs:
        print("Cleaning existing logs ...")
        for service_key in SERVICES:
            remove_logfile(service_key)

    for service_key in SERVICES:
        ssl = True
        try:
            url = SERVICES[service_key].url
            print(f"Pinging {SERVICES[service_key].name} ({url}) ...")
            resp = requests.get(url)
        except SSLError as e:
            ssl = False
            print("- Unable to verify SSL certificate; retrying without verifying ...")
            resp = requests.get(url, verify=False)
        code = resp.status_code
        new_status = "up" if resp.ok else "down"
        if not ssl:
            new_status += "-nossl"
        last_status = check_last_status(service_key)
        log_status(service_key, new_status, code)
        if last_status != new_status:
            print(f"- Status changed from {last_status} to {new_status}")
            send_telegram_message(service_key, new_status, code)
            send_discord_message(service_key, new_status, code)