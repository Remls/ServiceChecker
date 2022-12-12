import requests
from requests.exceptions import SSLError
from ping_classes import Service
import re
import os
import datetime
from config import SERVICES, TG_BOT_TOKEN, TG_CHAT_IDS, TG_MESSAGE_FORMAT, DISCORD_WEBHOOKS, DISCORD_MESSAGE_FORMAT


def send_telegram_message(service: Service, new_status = 'up', code = 200, ping_time = 0, silent = False):
    if not TG_BOT_TOKEN or not TG_CHAT_IDS:
        print("Telegram is not configured; skipping ...")
        return

    template = TG_MESSAGE_FORMAT[new_status]
    text = format_message(template, service, code, ping_time)
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

def send_discord_message(service: Service, new_status = 'up', code = 200, ping_time = 0):
    if not DISCORD_WEBHOOKS:
        print("Discord is not configured; skipping ...")
        return

    template = DISCORD_MESSAGE_FORMAT[new_status]
    text = format_message(template, service, code, ping_time)
    for webhook_url in DISCORD_WEBHOOKS:
        requests.post(
            webhook_url,
            json = {
                "content": text,
            }
        )

def format_message(template: str, service: Service, code = 200, ping_time = 0):
    template = re.sub(r"\$TAG\$", service.tag.value, template)
    template = re.sub(r"\$SERVICE\$", service.name, template)
    template = re.sub(r"\$CODE\$", str(code), template)
    template = re.sub(r"\$PING\$", str(ping_time), template)
    return template

def get_logfile_name(service: Service):
    return f"logs/{service.key}.log"

def remove_logfile(service: Service):
    log = get_logfile_name(service)
    if os.path.exists(log):
        os.remove(log)

def check_last_status(service: Service):
    log = get_logfile_name(service)
    if not os.path.exists(log):
        return None
    with open(log) as f:
        lines = f.readlines()
        if not lines:
            return None
        lines.reverse()
        for l in lines:
            if l:
                status = l.split(' - ')[1].strip()
                # Ping is optional, so we need to check if it exists
                if len(l.split(' - ')) > 3:
                    ping_time = l.split(' - ')[3].strip().replace('p', '')
                else:
                    ping_time = 0
                return status, ping_time
    return None

def log_status(service: Service, new_status = 'up', code = 200, ping_time = 0):
    log = get_logfile_name(service)
    timestamp = str(datetime.datetime.now())
    with open(log, 'a') as f:
        f.write(f"{timestamp} - {new_status} - {code} - p{ping_time}\n")


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
        last_status = check_last_status(service)
        log_status(service, new_status, code, ping_time)
        if last_status != new_status:
            print(f"- Status changed from {last_status} to {new_status}")
            send_telegram_message(service, new_status, code, ping_time)
            send_discord_message(service, new_status, code, ping_time)