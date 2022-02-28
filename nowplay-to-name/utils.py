def clean_text(text):
	text = text.replace("<","-")
	text = text.replace(">","-")
	return text

def genarate_new_name(user_name, current_play):
    current_track_name = current_play["item"]["name"]
    current_track_artist_list = current_play["item"]["artists"]
    current_track_artist_name_list = ""
    for artist in current_track_artist_list:
        current_track_artist_name_list +=artist["name"]
    track_display = current_track_name+"/"+current_track_artist_name_list
    target_name = (user_name+"🎵"+track_display)[:50]
    target_name = clean_text(target_name)
    return target_name