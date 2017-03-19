# Lars
Python script to record livestreams from Twitch.

Uses the [pythonNotify](https://github.com/mtverlee/pythonNotify) module to send notifications.

## Installation
To install this script, run the following command in a terminal with privileges.
```
git clone https://github.com/mtverlee/lars.git --recursive
sudo chmod a+x *.sh
./install.sh
```

## Use:
- Livestreams uses [Pushover](https://pushover.net/) notifications to notify you of events. Include your user token and app token under the 'Settings' section at the top of record.py.
- Include your Twitch API key under the 'Settings' section at the top of record.py.
- Include a list of Twitch usernames to check for streams under the 'Settings' section at the top of record.py.
