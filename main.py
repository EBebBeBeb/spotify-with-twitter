import os
import time
import signal
from driver.driver import *

global user_name
global tweepy_api

def keyboardInterruptHandler(signal, frame):
	try:
		tweepy_api.update_profile(name=user_name)
		exit(0)
	except:
		exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

tweepy_api = new_tweepy_client()
spotipy_client = new_spotipy_client()

try:
	screen_name = tweepy_api.get_settings()["screen_name"]
except: # reset access credential in case of auth failure.
	update_tweepy_access_token("","")
print(screen_name)
user = tweepy_api.get_user(screen_name=screen_name)

print("ctrl+c (SIGINT) to stop and get back to original name")

previous_name = ""
while(1):
	user_name = user._json["name"].split("🎵")[0]
	try:
		current_play = spotipy_client.current_playback()
		current_track_name = current_play["item"]["name"]
		current_track_artist_list = current_play["item"]["artists"]
		current_track_artist_name_list = ""
	except:
		print("Can't achieve Nowplaying")
		tweepy_api.update_profile(name=user_name)
		time.sleep(30)
		continue
	for artist in current_track_artist_list:
		current_track_artist_name_list +=artist["name"]
	track_display = current_track_name+"/"+current_track_artist_name_list
	target_name = (user_name+"🎵"+track_display)[:50]
	if previous_name != target_name:
		print("Updating to :",target_name)
		previous_name = target_name
		tweepy_api.update_profile(name=target_name)	
	time.sleep(30)
