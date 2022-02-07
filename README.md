# spotify-with-twitter
Wondering how to have fun with twitter and spotify  
Rough project for my hobby, plz let me know if something's wrong.

## Setting up credentials
To avoid API call limit, you should prepare your own application on [Twitter developer]("https://developer.twitter.com/en/portal/dashboard") and [Spotify API]("https://developer.spotify.com/dashboard/applications")
### Twitter API KEY
Create new standalone application and you can get `API_KEY` and `API_SECRET` add them to `TWEEPY` field of `credentials.json`.  
Let `ACCESS_TOKEN` and `ACCESS_TOKEN_SECRET` as `""` it will be automatically filled after your first authorization to the app.  
### Spotify INFO
Make new app on spotify api dashboard. You will get `CLIENT_ID` and `CLIENT_SECRET`. Also go to `EDIT SETTINGS` and write `REDIRECT_URI`  
It doesn't have to be valid.  
Add those data to `SPOTIPY` field of `credentials.json`

## Now play to twitter name
The only service for now.  
{username} -> {username}🎵{title}/{artist}  
limit of the username is 50.  
When SIGINT detected,  
{username}🎵{title}/{artist} -> {username}  
