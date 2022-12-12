import os
import requests
from requests.exceptions import SSLError
from ping_classes import PingResponse
from file_functions import remove_logfile, check_last_status, log_status
from message_functions import send_telegram_message, send_discord_message, send_all_statuses_to_telegram
from config import SERVICES


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
