import requests
from requests.exceptions import SSLError
import re
import os
import datetime
from config import BOT_TOKEN, CHAT_ID, SERVICES, MESSAGE_FORMAT


def send_telegram_message(service_name: str, new_status = 'up', code = 200, silent = False):
    text = re.sub(r"\$SERVICE\$", service_name, MESSAGE_FORMAT[new_status])
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params = {
            "chat_id": CHAT_ID,
            "text": f"{text} ({code})",
            "parse_mode": "HTML",
            "disable_notification": silent
        }
    )

def get_logfile_name(service_name: str):
    return f"logs/{service_name}.log"

def check_last_status(service_name: str):
    log = get_logfile_name(service_name)
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

def log_status(service_name: str, new_status = 'up', code = 200):
    log = get_logfile_name(service_name)
    timestamp = str(datetime.datetime.now())
    with open(log, 'a') as f:
        f.write(f"{timestamp} - {new_status} - {code}\n")

if __name__ == '__main__':
    for service in SERVICES:
        try:
            url = SERVICES[service]
            print(f"Pinging {service} ({url}) ...")
            resp = requests.get(url)
        except SSLError as e:
            print("- Unable to verify SSL certificate; retrying without verifying ...")
            resp = requests.get(url, verify=False)
        code = resp.status_code
        new_status = "up" if resp.ok else "down"
        last_status = check_last_status(service)
        log_status(service, new_status, code)
        if last_status != new_status:
            send_telegram_message(service, new_status, code)