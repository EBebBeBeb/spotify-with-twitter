import tweepy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import webbrowser

def new_tweepy_client():
	API_KEY, API_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET  = get_tweepy_credentials()
	if ACCESS_TOKEN != "" and ACCESS_TOKEN_SECRET != "" :
		auth = tweepy.OAuth1UserHandler( API_KEY, API_SECRET ,ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
		tweepy_api = tweepy.API(auth)
	else:
		ACCESS_TOKEN,ACCESS_TOKEN_SECRET = get_tweepy_new_access_token(API_KEY, API_SECRET)
		auth = tweepy.OAuth1UserHandler( API_KEY, API_SECRET ,ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
		tweepy_api = tweepy.API(auth)
	return tweepy_api

def new_spotipy_client():
	SPOTIPY_REDIRECT_URI,SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET = get_spotipy_credentials()
	os.environ["SPOTIPY_REDIRECT_URI"] = SPOTIPY_REDIRECT_URI
	os.environ["SPOTIPY_CLIENT_ID"]=SPOTIPY_CLIENT_ID
	os.environ["SPOTIPY_CLIENT_SECRET"]=SPOTIPY_CLIENT_SECRET
	scope = "user-read-playback-state"
	spotipy_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
	return spotipy_client

def get_tweepy_credentials():
	raw = open("./credentials.json",'r')
	data = json.load(raw)
	return data["TWEEPY"]["API_KEY"], data["TWEEPY"]["API_SECRET"], data["TWEEPY"]["ACCESS_TOKEN"], data["TWEEPY"]["ACCESS_TOKEN_SECRET"]

def get_tweepy_new_access_token(API_KEY, API_SECRET):
	oauth1_user_handler = tweepy.OAuth1UserHandler( API_KEY, API_SECRET, callback="oob" )
	webbrowser.open_new(oauth1_user_handler.get_authorization_url(signin_with_twitter=True))
	PIN = input("PIN :" )
	ACCESS_TOKEN,ACCESS_TOKEN_SECRET = oauth1_user_handler.get_access_token( PIN )
	update_tweepy_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
	return ACCESS_TOKEN,ACCESS_TOKEN_SECRET

def update_tweepy_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET):
	with open("./credentials.json",'r+') as raw:
	    data = json.load(raw)
	    data["TWEEPY"]["ACCESS_TOKEN"] = ACCESS_TOKEN 
	    data["TWEEPY"]["ACCESS_TOKEN_SECRET"] = ACCESS_TOKEN_SECRET
	    raw.seek(0)
	    json.dump(data, raw, indent=4)
	    raw.truncate()

def get_spotipy_credentials():
	with open("./credentials.json",'r') as raw:
		data = json.load(raw)
	return data["SPOTIPY"]["SPOTIPY_REDIRECT_URI"], data["SPOTIPY"]["SPOTIPY_CLIENT_ID"], data["SPOTIPY"]["SPOTIPY_CLIENT_SECRET"]
