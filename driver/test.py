import sys
import spotipy
import spotipy.util as util
import json
import webbrowser
import tweepy
import os

def get_spotipy_credentials():
    with open("../credentials.json",'r') as raw:
        data = json.load(raw)
        for a in data["USERS"]:
            print(a)
    return data["SPOTIPY"]["SPOTIPY_REDIRECT_URI"], data["SPOTIPY"]["SPOTIPY_CLIENT_ID"], data["SPOTIPY"]["SPOTIPY_CLIENT_SECRET"]

def get_tweepy_credentials():
    raw = open("../credentials.json",'r')
    data = json.load(raw)
    return data["TWEEPY"]["API_KEY"], data["TWEEPY"]["API_SECRET"]

def update_user_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET, SPOTIPY_TOKEN):
    user_block = {}
    user_block["TWEEPY_ACCESS_TOKEN"] = ACCESS_TOKEN
    user_block["TWEEPY_ACCESS_TOKEN_SECRET"] = ACCESS_TOKEN_SECRET
    user_block["SPOTIPY_TOKEN"] = SPOTIPY_TOKEN

    with open("../credentials.json",'r+') as raw:
        data = json.load(raw)
        data["USERS"]["NAME"]= user_block
        raw.seek(0)
        json.dump(data, raw, indent=4)
        raw.truncate()

def get_tweepy_new_access_token(API_KEY, API_SECRET):
    oauth1_user_handler = tweepy.OAuth1UserHandler( API_KEY, API_SECRET, callback="oob" )
    webbrowser.open_new(oauth1_user_handler.get_authorization_url(signin_with_twitter=True))
    PIN = input("PIN :" )
    ACCESS_TOKEN,ACCESS_TOKEN_SECRET = oauth1_user_handler.get_access_token( PIN )
    return ACCESS_TOKEN,ACCESS_TOKEN_SECRET

scope = "user-read-playback-state"
SPOTIPY_REDIRECT_URI,SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET = get_spotipy_credentials()
os.environ["SPOTIPY_REDIRECT_URI"] = SPOTIPY_REDIRECT_URI
os.environ["SPOTIPY_CLIENT_ID"]=SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"]=SPOTIPY_CLIENT_SECRET

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

TWEEPY_API_KEY, TWEEPY_API_KEY_SECRET = get_tweepy_credentials()
ACCESS_TOKEN,ACCESS_TOKEN_SECRET = get_tweepy_new_access_token(TWEEPY_API_KEY, TWEEPY_API_KEY_SECRET)
token = util.prompt_for_user_token(username, scope)

update_user_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET, token)