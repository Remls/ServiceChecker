# Service Checker

Ping to see if services are up, and send results to Telegram and/or Discord.

### Setup

- Needs Python 3
- Install requirements: `pip install -r requirements.txt`
- Copy `config.template.py` to `config.py`, and fill in environment variables + list of services
- Set up cron:

```sh
crontab -e
| */n * * * * cd /your/folder/location && python3 ping.py
# (where n is the minute interval you wish to ping with)
```

- Start cron:

```sh
service cron start
# or
service cron restart
```

### Pruning

```sh
python3 ping.py --prune
```

This will delete all logs older than 24 hours.

### Start from scratch

```sh
python3 ping.py --clean
```

This will delete all logs and any stored data, and then start pinging again.