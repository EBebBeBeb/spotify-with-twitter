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

def clean_text(text):
	text = text.replace("<","-")
	text = text.replace(">","-")
	return text

signal.signal(signal.SIGINT, keyboardInterruptHandler)

tweepy_api = []
spotipy_client = []
twitter_user_name_list = []

print(get_user_list())
for name in get_user_list():
	TWEEPY_ACCESS_TOKEN, TWEEPY_ACCESS_TOKEN_SECRET, SPOTIPY_TOKEN = get_user_token(name)
	tweepy_tmp_client = new_tweepy_client(TWEEPY_ACCESS_TOKEN,TWEEPY_ACCESS_TOKEN_SECRET)
	try:
		screen_name = tweepy_tmp_client.get_settings()["screen_name"]
	except: # reset access credential in case of auth failure.
		update_tweepy_access_token("","")
	print(screen_name)
	twitter_user_name_list.append(tweepy_tmp_client.get_user(screen_name=screen_name))
	
	tweepy_api.append(tweepy_tmp_client)
	spotipy_client.append(new_spotipy_client(SPOTIPY_TOKEN))


print("ctrl+c (SIGINT) to stop and get back to original name")

previous_name = []
for i in range(len(twitter_user_name_list)):
	previous_name.append("")

while(1):
	for i in range(len(twitter_user_name_list)):
		user_name = twitter_user_name_list[i]._json["name"].split("🎵")[0]
		try:
			current_play = spotipy_client[i].current_playback()
			current_track_name = current_play["item"]["name"]
			current_track_artist_list = current_play["item"]["artists"]
			current_track_artist_name_list = ""
		except:
			print("Can't achieve Nowplaying for username : ",user_name)
			tweepy_api[i].update_profile(name=user_name)
			continue
		for artist in current_track_artist_list:
			current_track_artist_name_list +=artist["name"]
		track_display = current_track_name+"/"+current_track_artist_name_list
		target_name = (user_name+"🎵"+track_display)[:50]
		target_name = clean_text(target_name)
		if previous_name[i] != target_name:
			print("Updating to :",target_name)
			previous_name[i] = target_name
			try:
				tweepy_api[i].update_profile(name=target_name)
			except:
				continue
	time.sleep(30)

