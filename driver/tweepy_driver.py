import tweepy
import json
import os
import webbrowser

def new_tweepy_client(ACCESS_TOKEN="",ACCESS_TOKEN_SECRET=""):
	API_KEY, API_SECRET = get_tweepy_credentials()
	if ACCESS_TOKEN != "" and ACCESS_TOKEN_SECRET != "" :
		auth = tweepy.OAuth1UserHandler( API_KEY, API_SECRET ,ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
		tweepy_api = tweepy.API(auth)
	else:
		ACCESS_TOKEN,ACCESS_TOKEN_SECRET = get_tweepy_new_access_token(API_KEY, API_SECRET)
		auth = tweepy.OAuth1UserHandler( API_KEY, API_SECRET ,ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
		tweepy_api = tweepy.API(auth)
	return tweepy_api

def get_tweepy_credentials():
	raw = open("../credentials.json",'r')
	data = json.load(raw)
	return data["TWEEPY"]["API_KEY"], data["TWEEPY"]["API_SECRET"]

def get_tweepy_new_access_token(API_KEY, API_SECRET):
	oauth1_user_handler = tweepy.OAuth1UserHandler( API_KEY, API_SECRET, callback="oob" )
	webbrowser.open_new(oauth1_user_handler.get_authorization_url(signin_with_twitter=True))
	PIN = input("PIN :" )
	ACCESS_TOKEN,ACCESS_TOKEN_SECRET = oauth1_user_handler.get_access_token( PIN )
	update_tweepy_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
	return ACCESS_TOKEN,ACCESS_TOKEN_SECRET

def update_tweepy_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET):
	with open("../credentials.json",'r+') as raw:
		data = json.load(raw)
		data["USERS"]["NAME"]["TWEEPY_ACCESS_TOKEN"] = ACCESS_TOKEN 
		data["USERS"]["NAME"]["TWEEPY_ACCESS_TOKEN_SECRET"] = ACCESS_TOKEN_SECRET
		raw.seek(0)
		json.dump(data, raw, indent=4)
		raw.truncate()

