import os
from ping_classes import Service, PingResponse


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
                return l.split(' - ')[1].strip()
    return None

def log_status(ping_response: PingResponse):
    log = get_logfile_name(ping_response.service)
    with open(log, 'a') as f:
        f.write(f"{ping_response}\n")
