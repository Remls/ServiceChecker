import os
from ping_classes import Service, PingResponse

MESSAGE_ID_FILE = "logs/__msg_id"


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

def get_message_ids():
    if not os.path.exists(MESSAGE_ID_FILE):
        return {}
    with open(MESSAGE_ID_FILE) as f:
        lines = f.readlines()
        if not lines:
            return {}
        ids = {}
        for l in lines:
            if l:
                # chat_id, msg_id
                chat_id = l.split(' - ')[0].strip()
                msg_id = l.split(' - ')[1].strip()
                ids[chat_id] = msg_id
        return ids

def set_message_id(chat_id, msg_id):
    ids = get_message_ids()
    ids[chat_id] = msg_id
    with open(MESSAGE_ID_FILE, 'w') as f:
        for chat_id, msg_id in ids.items():
            f.write(f"{chat_id} - {msg_id}\n")

def wipe_message_ids():
    """Remove all message IDs from file, but keep the file itself"""
    with open(MESSAGE_ID_FILE, 'w') as f:
        pass
