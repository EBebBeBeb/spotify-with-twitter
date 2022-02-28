import os
import time
import signal
from driver.driver import *

global twitter_user_name_list
global tweepy_api

def keyboardInterruptHandler(signal, frame):
	try:
		i=0
		for api in tweepy_api:
			api.update_profile(name=twitter_user_name_list[i]._json["name"].split("🎵")[0])
			i+=1
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
spotipy_oauth2_client_list = []
user_name_list = []
twitter_user_name_list = []
SPOTIPY_TOKEN_LIST = []

for name in get_user_list():
	user_name_list.append(name)
	spotipy_oauth2_client_list.append(spotipy_oauth2_client(name))
	TWEEPY_ACCESS_TOKEN, TWEEPY_ACCESS_TOKEN_SECRET, SPOTIPY_TOKEN = get_user_token(name)
	SPOTIPY_TOKEN_LIST.append(SPOTIPY_TOKEN)
	tweepy_tmp_client = new_tweepy_client(TWEEPY_ACCESS_TOKEN,TWEEPY_ACCESS_TOKEN_SECRET)
	try:
		screen_name = tweepy_tmp_client.get_settings()["screen_name"]
	except: # reset access credential in case of auth failure.
		update_tweepy_access_token("","")
	print(screen_name)
	twitter_user_name_list.append(tweepy_tmp_client.get_user(screen_name=screen_name))
	
	tweepy_api.append(tweepy_tmp_client)
	spotipy_client.append(new_spotipy_client(SPOTIPY_TOKEN))

	token_info = spotipy_oauth2_client(name).get_cached_token()

print("ctrl+c (SIGINT) to stop and get back to original name")

previous_name = [""+str(i) for i in range(len(twitter_user_name_list))]

while(1):
	for i in range(len(twitter_user_name_list)):
		try:
			screen_name = tweepy_api[i].get_settings()["screen_name"]
			print(screen_name)
			user_data=tweepy_api[i].get_user(screen_name=screen_name)
			user_name = user_data._json["name"].split("🎵")[0]
			print(user_name)
		except:
			continue		
		try:
			current_play = spotipy_client[i].current_playback()
		except spotipy.client.SpotifyException:
			print("Token_expired")
			try:
				token_info = spotipy_oauth2_client_list[i].get_cached_token()
				token_info = spotipy_oauth2_client_list[i].refresh_access_token(token_info['refresh_token'])
				access_token = token_info['access_token']
				update_spotipy_access_token(user_name_list[i],access_token)
				spotipy_client[i] = new_spotipy_client(access_token)
			except:
				continue
			try:
				current_play = spotipy_client[i].current_playback()
			except:
				continue
		except:
			continue
		try:
			current_track_name = current_play["item"]["name"]
			current_track_artist_list = current_play["item"]["artists"]
			current_track_artist_name_list = ""
		except:
			print("Can't achieve Nowplaying for username : ",user_name)
			if user_data._json["name"] != user_name:
				tweepy_api[i].update_profile(name=user_name)
			continue
		for artist in current_track_artist_list:
			current_track_artist_name_list +=artist["name"]
		track_display = current_track_name+"/"+current_track_artist_name_list
		target_name = (user_name+"🎵"+track_display)[:50]
		target_name = clean_text(target_name)
		print(previous_name)
		if previous_name[i] != target_name:
			print("Updating to :",target_name)
			previous_name = [name.replace(previous_name[i],target_name) for name in previous_name]
			try:
				tweepy_api[i].update_profile(name=target_name)
			except:
				continue
	time.sleep(30)

