import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

"""Scraping Billboard 100"""
users_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{users_input}")

soup = BeautifulSoup(response.text, 'html.parser')
song_names_h3 = soup.find_all("h3", class_="a-no-trucate")
song_names = [song.getText().strip() for song in song_names_h3]
# print(song_names)


"""Spotify Authentication"""
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id="e93a4d5760f6484d84b2d12f9787dddf",
        client_secret=Your client secret
        redirect_uri="http://example.com",
        show_dialog=True,
        cache_path="token.txt"
    ))
user_id = sp.current_user()["id"]
# print(user_id)


"""Searching Spotify for songs by title"""
song_uris = []
year = users_input.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
        # print(song_uris)

"""Creating a new private playlist in Spotify"""
playlist = sp.user_playlist_create(user=user_id, name=f"{users_input} Billboard 100", public=False)
# print(playlist["id"])

"""Adding songs found into the new playlist"""
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
