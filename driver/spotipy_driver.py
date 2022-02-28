import json
import os
import spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

def new_spotipy_client(TOKEN=""):
	SPOTIPY_REDIRECT_URI,SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET = get_spotipy_credentials()
	os.environ["SPOTIPY_REDIRECT_URI"] = SPOTIPY_REDIRECT_URI
	os.environ["SPOTIPY_CLIENT_ID"]=SPOTIPY_CLIENT_ID
	os.environ["SPOTIPY_CLIENT_SECRET"]=SPOTIPY_CLIENT_SECRET
	scope = "user-read-playback-state"
	spotipy_client = spotipy.Spotify(auth=TOKEN)
	return spotipy_client

def update_spotipy_access_token(NAME,SPOTIPY_TOKEN):
	with open("../credentials.json",'r+') as raw:
		data = json.load(raw)
		data["USERS"][NAME]["SPOTIPY_TOKEN"] = SPOTIPY_TOKEN 
		raw.seek(0)
		json.dump(data, raw, indent=4)
		raw.truncate()

def get_spotipy_credentials():
	with open("../credentials.json",'r') as raw:
		data = json.load(raw)
	return data["SPOTIPY"]["SPOTIPY_REDIRECT_URI"], data["SPOTIPY"]["SPOTIPY_CLIENT_ID"], data["SPOTIPY"]["SPOTIPY_CLIENT_SECRET"]

def get_spotipy_new_token():
	with open("../credentials.json",'r') as raw:
		data = json.load(raw)
	return data["SPOTIPY"]["SPOTIPY_REDIRECT_URI"], data["SPOTIPY"]["SPOTIPY_CLIENT_ID"], data["SPOTIPY"]["SPOTIPY_CLIENT_SECRET"]

def new_spotipy_oauth2_client(name):
	path = '../driver/spotipy_cache/.cache-'+name
	scope = "user-read-playback-state"
	SPOTIPY_REDIRECT_URI,SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET = get_spotipy_credentials()
	return oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=scope,cache_path=path)

def refresh_spotipy_client(oauth_handler, name):
	cached_token = oauth_handler.get_cached_token()
	refreshed_token = oauth_handler.refresh_access_token(cached_token['refresh_token'])
	access_token = refreshed_token['access_token']
	update_spotipy_access_token(name,access_token)
	return new_spotipy_client(access_token)