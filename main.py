import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ['SPOTIPY_CLIENT_ID'],
        client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
        redirect_uri='http://example.com',
        scope='playlist-modify-private',
        cache_path='token.txt',
        show_dialog=True
    )
)
# Get the user ID
user_id = sp.current_user()['id']

# Insert a date
user_year = input('Which year do you want to travel to?\n\x1B[3m(Type the data in this format YYYY-MM-DD)\n')

# Scrap the top 100 songs of a given date.
URL = f"https://www.billboard.com/charts/hot-100/{user_year}/"
response = requests.get(URL)
billboard_webpage = response.text
soup = BeautifulSoup(billboard_webpage, 'html.parser')
# Select the titles of the songs.
top_100 = soup.select(selector="li h3")
song_list = [song.getText().strip("\n") for song in top_100[:100]]


uri_list = []
for song in song_list:
    try:
        # Get the uri's from spotify using the title of the songs and spotipy library.
        uri = sp.search(q=f"track:{song} "
                          f"year:{user_year.split('-')[0]}",
                        type='track')['tracks']['items'][0]['uri']
        # Add them to a list.
        uri_list.append(uri)
    except IndexError:
        print('No song found with that title.')
        pass

# Create a playlist.
playlist = sp.user_playlist_create(user=user_id,
                                   name=f"{user_year} Billboard 100",
                                   public=False)
# Add the songs to the playlist.
sp.playlist_add_items(playlist_id=playlist['id'],
                      items=uri_list)
