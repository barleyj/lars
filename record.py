"""

Livestream Recorder
By Matt VerLee

mtverlee@mavs.coloradomesa.edu
https://github.com/mtverlee

"""

#!/usr/bin/env

import threading
import os
import time
from termcolor import colored
import requests
import json
import urllib2
import traceback
import datetime
import notifications.main as notifications
import better_exceptions
better_exceptions.MAX_LENGTH = None

# Settings.
appToken = ""
userToken = ""
twitchAPIKey = ""
periodInMinutes = 5
minRecordPeriodInMinutes = 10
streamers = []
# Available quality settings:  audio, source, high, low, medium, mobile
recordQuality = 'medium'


# Definitions.
locks = []

# Check if livestreamer is installed.BaseException
def checkLivestreamer():
	livestreamerInstalled = os.system('dpkg -s livestreamer | grep Status >/dev/null 2>&1')
	if livestreamerInstalled == 0:
		return True
	else:
		return False

# Check for streams and launch threads to record them if found.
def checkForStreams(streamers, periodInMinutes):
	while True:
		# Formulate messages.
		currentTimeDate = str(time.strftime("%c"))
		searchStartMessage = "Started checking for streams at " + currentTimeDate + "."
		searchEndMessage = "Finished checking for streams at " + currentTimeDate + "."

		# Check for streams.
		print(colored(searchStartMessage, 'blue'))
		for name in streamers:
			try:
				jsonInfo = requests.get('https://api.twitch.tv/kraken/streams/' + name + '?client_id=' + twitchAPIKey, timeout=15)
				streamerJson = json.loads(jsonInfo.content)
				if streamerJson['stream'] == None:
					print(colored('No streams found for streamer "%s".' % (name), 'yellow'))
				else:
					print(colored('Stream was found for streamer "%s".' % (name), 'green'))
					threading.Thread(target=recordStream, args=(name, locks)).start()
			except urllib2.URLError as e:
					print(colored('Error occurred for streamer "' + name + '" - ' + str(e.reason) + '.', 'red'))
					continue
			except urllib2.HTTPError as e:
					print(colored('Error occurred for streamer "' + name + '" - ' + str(e.reason) + '.', 'red'))
					continue
			except Exception:
					print(colored('Error occurred for streamer "' + name + '" - ' + str(traceback.format_exc()), 'red'))
					continue
		currentTimeDate = str(time.strftime("%c"))
		print(colored(searchEndMessage, 'blue'))
		print(colored('Sleeping for %s minutes.' % (periodInMinutes), 'blue'))
		time.sleep(periodInMinutes * 60)

# Stream record function.
def recordStream(name, locks):
	if name in locks:
		print(colored("Failed to start thread for %s - already locked!" % (name), 'blue'))
	else:
		# Formulate messages.
		lockStartMessage = 'Lock for streamer "' + name + '" has been set.'
		threadStartMessage = 'Thread for streamer "' + name + '" has started.'
		noDirectoryMessage = 'Directory for "' + name + '" was not found - a new one was created.'
		badPermissionsMessage = 'Directory for streamer "' + name + '" is not writable - streams will fail to be written!'
		lockEndMessage = 'Lock for streamer "' + name + '" has been unset.'
		threadEndMessage = 'Thread for streamer "' + name + '" has closed.'

		# Record.
		print(colored(threadStartMessage, 'blue'))
		locks.append(name)
		print(colored(lockStartMessage, 'blue'))
		print(colored("Currently locked - %s" % (locks), 'blue'))
		dateTimeNow = str(time.strftime("%m_%d_%Y_%H_%M"))
		path = name + "/"
		if not os.path.exists(path):
			os.makedirs(path)
			print(colored(noDirectoryMessage, 'blue'))
		if not os.access(path, os.W_OK):
			print(colored(badPermissionsMessage, 'red'))
		totalPath = path + dateTimeNow + ".mp4"
		cmd = "livestreamer --yes-run-as-root --hds-segment-attempts=5 --hds-segment-threads=10 --http-header=Client-ID=%s http://www.twitch.tv/%s %s --output %s" % (twitchAPIKey, name, recordQuality, totalPath)
		os.system(cmd)
		if os.path.isfile(totalPath):
			notifications.sendPushoverNotification(appToken, userToken, 'A livestream by streamer "' + name + '" has been recorded.', 'Livestreams')
		else:
			print(colored('Failed to record livestream for streamer "%s" - Twitch API is likely updating the stream status.' % (name), 'blue'))
		locks.remove(name)
		print(colored(lockEndMessage, 'blue'))
		print(colored("Currently locked - %s" % (locks), 'blue'))
		print(colored(threadEndMessage, 'blue'))

# Main start.
if __name__ == '__main__':
	notifications.sendPushoverNotification(appToken, userToken, 'Livestream recording is starting.', 'Livestreams')
	if checkLivestreamer():
		checkForStreams(streamers, periodInMinutes)
	else:
		print(colored("Fatal error! - Livestreamer is necessary and is not installed.", 'red'))

