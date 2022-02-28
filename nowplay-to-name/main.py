
import os
import time
import signal
import os,sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from driver.tweepy_driver import *
from driver.spotipy_driver import *
from driver.common import *
from utils import *

global twitter_user_name_list
global tweepy_api

def keyboardInterruptHandler(signal, frame):
	for i, api in enumerate(tweepy_api):
		try:
			api.update_profile(name=twitter_user_name_list[i]._json["name"].split("🎵")[0])
		except:
			sys.stderr.write("Can't update name to : "+twitter_user_name_list[i]._json["name"].split("🎵")[0])
			continue
	exit(0)

def main():
	signal.signal(signal.SIGINT, keyboardInterruptHandler)

	tweepy_api_list, twitter_user_name_list, spotipy_client_list, spotipy_oauth2_client_list, user_name_list = initialize_client_list()

	print("ctrl+c (SIGINT) to stop and get back to original name")

	previous_name = [""+str(i) for i in range(len(twitter_user_name_list))]

	while(1):
		for i in range(len(twitter_user_name_list)):
			try:
				screen_name = tweepy_api_list[i].get_settings()["screen_name"]
				user_data=tweepy_api_list[i].get_user(screen_name=screen_name)
				user_name = user_data._json["name"].split("🎵")[0]
				current_play = spotipy_client_list[i].current_playback()
			except spotipy.client.SpotifyException:
				print("Token_expired")
				try:
					spotipy_client_list[i]=refresh_spotipy_client(spotipy_oauth2_client_list[i], user_name_list[i])
					current_play = spotipy_client_list[i].current_playback()
					print("Token_regenerated")
				except:
					sys.stderr.write("Token_regeneration_failed")
					continue
			except:
				sys.stderr.write("Can't get user data")
				continue
			try:
				target_name=genarate_new_name(user_name, current_play)
			except:
				print("Can't achieve Nowplaying for username : ",user_name) # Not as stderr
				if user_data._json["name"] != user_name:
					tweepy_api_list[i].update_profile(name=user_name)
				continue
			if previous_name[i] != target_name:
				print("Updating to :",target_name)
				previous_name = [name.replace(previous_name[i],target_name) for name in previous_name]
				try:
					tweepy_api_list[i].update_profile(name=target_name)
				except:
					sys.stderr.write("Can't update name to : "+target_name)
					continue
		print(previous_name)
		time.sleep(30)

if __name__ == "__main__":
    main()