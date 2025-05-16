import requests
import os
import json
from urllib.request import urlopen #Abridor de URL
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime

#Scraper


url = "https://hypem.com/popular/" #Pagina inicial do hype machine

pagina = urlopen(url) #urlopen() returns an HTTPResponse object:

html_bytes = pagina.read() # .read() retorna bytes de html
html = html_bytes.decode("utf-8")

soup = BeautifulSoup(html, 'html.parser')
script_tag = soup.find("script",  {'type': "application/json"})


json_text = script_tag.text
try:
    data = json.loads(json_text)
    # Process the extracted JSON data
except json.JSONDecodeError:
        print(f"Could not decode JSON: {json_text}")
print(data)


dict={}
uri_list = []

for i in range(len(data["tracks"])):
     #Pegando artista, musica e URI spotify do json e add no dict
    if "spotify_uri" in data["tracks"][i]:
        dict.update(
            {data["tracks"][i]["artist"]: { 
                 "Track" : data["tracks"][i]["song"], 
                 "Spotify": data["tracks"][i]["spotify_uri"] 
                 }})
        uri_list.append(data["tracks"][i]["spotify_uri"])
print(dict)



print(uri_list)


#Spotify Client Credentials Flow
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='a4da6467f4454db59104caff0d0754ca',
    client_secret='6d2c28fce2164884acbd0f41d00ffb2e',
    redirect_uri='http://127.0.0.1:5050',
    scope= "playlist-modify-private playlist-modify-public"
))

user = sp.current_user()

today = datetime.date.today()
date = today.strftime("%Y-%m-%d")


playlist_name = "Hypem dscvr" + " " + date
items = []
playlist = sp.user_playlist_create(user["id"], playlist_name, public=False, collaborative=False, description='') #Creates a playlist for a user
playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id, uri_list, position=None)