import pprint
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

DATE = input("what data do you want to travel to? in this format : YYYY-MM-DD : ")
URL = f"https://www.billboard.com/charts/hot-100/{DATE}/"

# parse billboard webpage for all song titles
response = requests.get(URL)
billboard_webpage = response.text
soup = BeautifulSoup(billboard_webpage, "html.parser")
songs = soup.find_all(name='h3', class_="a-no-trucate")
song_titles = [song.getText().strip() for song in songs]

# spotify authentication and get user id
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.environ["SPOTIPY_CLIENT_ID"],
        client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

# get song uris from spotify
year = DATE.split("-")[0]
song_title_uris = []
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_title_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# creating playlist and adding songs
playlist = sp.user_playlist_create(os.environ["USER_ID"], f"Udemy_Billboard_100_{DATE}", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_title_uris)

