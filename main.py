from bs4 import BeautifulSoup
import requests
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


CLIENT_ID = "bda6d485f6ee4ae295c0128716a4b7f2"
CLIENT_SECRET = "1b22d482ac044945bcd5def48e8eb1ce"
REDIRECT_URI = "http://example.com"
SCOPE = "playlist-modify-private"

# Take User Input
# user_input = input("What date(YYYY-MM-DD) do you want to be transported to?: ")
# URL = f"https://www.billboard.com/charts/hot-100/{user_input}"
URL = "https://www.billboard.com/charts/hot-100/2012-03-31"

# Scrape Top 100
webpage = requests.get(url=URL)
website_content = webpage.text
soup = BeautifulSoup(website_content, "html.parser")

titles_tags = soup.select(selector="li ul li h3")
songs_list = [tag.getText().strip() for tag in titles_tags]
# print(songs_list)

# why did we use select instead of select_all?
#   Because select gives us all occurrences instead of the first one.

# Authenticate with Spotify using Spotipy
CODE="BQBpFmn1sizcliGHVnL8kI-K6F9TtEYZ6QWavoZOCZJUyYBSWTPWr7pxMUmXV8ZFXNe_B1DN3oM50kwDrobPkXws9MFqqy7KAHv9mc5zl7wAzRvnbOg_f7-DB4g84rfgHTJYwqxsvHp6uLfrVte0xIWBPd2EeLcErbPGYHXr34t6_5hox42aiz8lRTGwS37R1ntHsczuIv6KMPPgjGlyvXsVqiuZkUCNIDkZZw"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True,
))

user_id = sp.current_user()['id']

# Search for Songs
songs_uri_list = []
for song in songs_list:
    # try:
    song_details = sp.search(q=f"track: {song} year: {2012}", type="track", limit=1)
    try:
        song_uri = song_details['tracks']['items'][0]['uri']
        songs_uri_list.append(song_uri)
    except IndexError:
        print(f"Sorry {song} does not exist in Spotify.--Skipped--.")

print(songs_uri_list)

# Create a playlist
playlist_id = sp.user_playlist_create(user=user_id, name="2012-03-31 Billboard 100", public=False)['id']
pprint(playlist_id)
sp.playlist_add_items(playlist_id=playlist_id, items=songs_uri_list)



# ----------------------------------------------------NOTES-------------------------------------------------------------
# Spotify authentication is very complicated, so we will use Spotify from pypi
# (*) A real developer figures out challenges by reading documentations

# (*) Use EAFP






