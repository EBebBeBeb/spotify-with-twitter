import json
from driver.spotipy_driver import new_spotipy_client, new_spotipy_oauth2_client
from driver.tweepy_driver import new_tweepy_client, update_tweepy_access_token


def get_user_token(username):
	with open("../credentials.json",'r') as raw:
		data = json.load(raw)
	return data["USERS"][username]["TWEEPY_ACCESS_TOKEN"], data["USERS"][username]["TWEEPY_ACCESS_TOKEN_SECRET"], data["USERS"][username]["SPOTIPY_TOKEN"]

def get_user_list():
	with open("../credentials.json",'r') as raw:
		data = json.load(raw)
	return data["USERS"]

def initialize_client_list():
	tweepy_api_list = []
	twitter_user_name_list = []
	spotipy_client_list = []
	spotipy_oauth2_client_list = []
	user_name_list = []

	for name in get_user_list():
		user_name_list.append(name)
		spotipy_oauth2_client_list.append(new_spotipy_oauth2_client(name))
		TWEEPY_ACCESS_TOKEN, TWEEPY_ACCESS_TOKEN_SECRET, SPOTIPY_TOKEN = get_user_token(name)
		tweepy_tmp_client = new_tweepy_client(TWEEPY_ACCESS_TOKEN,TWEEPY_ACCESS_TOKEN_SECRET)
		try:
			screen_name = tweepy_tmp_client.get_settings()["screen_name"]
		except: # reset access credential in case of auth failure.
			update_tweepy_access_token("","")
		print(screen_name)
		twitter_user_name_list.append(tweepy_tmp_client.get_user(screen_name=screen_name))
		
		tweepy_api_list.append(tweepy_tmp_client)
		spotipy_client_list.append(new_spotipy_client(SPOTIPY_TOKEN))
	return tweepy_api_list, twitter_user_name_list, spotipy_client_list, spotipy_oauth2_client_list, user_name_list