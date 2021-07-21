import spotipy
from spotipy import util

scope = 'streaming,user-read-playback-state,user-modify-playback-state,user-read-recently-played,user-top-read,user-read-playback-position,playlist-modify-private'

client_id = 'not for u'
client_secret = 'not for u'

Token = util.prompt_for_user_token(
            'Q',
            scope,
            client_id=client_id ,
            client_secret=client_secret,
            redirect_uri='https://www.google.com/'
)

sp = spotipy.Spotify(auth=Token)

last = sp.current_user_recently_played(limit=5)


# input(last_fifty)
songs = []

for song in last['items']:
    songs.append(song['track']['uri'])
    print(song['track']['name']+"   uri:  "+song['track']['uri'])

raw_recs = sp.recommendations(seed_tracks=songs,limit=100)

recs = []

for song in raw_recs['tracks']:
    recs.append(song['uri'])

url = "https://open.spotify.com/playlist/7acL1ds5wSC9EQnxsSsEnq?si=ee07763c88994a35"


sp.playlist_replace_items(url, recs)

