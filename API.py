from flask_restful import Resource, request
from spotipy import util
from Database import Database
import pickle, spotipy, random, json


class Resources(Resource):

    def __init__(self):
        self.scope = 'streaming,user-read-playback-state,user-modify-playback-state,user-read-recently-played,user-top-read,user-read-playback-position,playlist-modify-private'
        self.device_id = None

        self.token = util.prompt_for_user_token('Q')
        self.sp = spotipy.Spotify(auth=self.token)

        self.DB = Database(self.sp)

        self.top_artists = self.sp.current_user_top_artists()['items']
        self.top_tracks = self.sp.current_user_top_tracks()['items']
        try:
            self.rec = pickle.load(open('cache/rec.p', 'rb'))
        except:
            self.rec = None
        
    def get(self, command):
        
        if command == 'playlists':
            playlists = None
            try:
                playlists = pickle.load(open('cache/playlists.p', 'rb+'))
            except:
                with self.sp.current_user_playlists() as reply:
                    print(reply)
                    playlists = json.encoder(reply)
                    pickle.dump(playlists, open('cache/playlists.p', 'wb+'))

            return playlists

        elif command == 'token':
            try:
                return {"token": self.token, "refresh": 'None'}
            except: 
                return {"token": "none", "refresh": "none"}

        elif command == 'Search':
            state = json.loads(request.data)
            self.DB.Search(state['Query'], state['ReturnAmt'], state['Type'])
            

        else:
            return {"command": "invalid"}

    def post(self, command):

        state = json.loads(request.data)

        if command == 'player_state':
            self.DB.GetSpotifyHistory()
            pickle.dump((state['track_window']['current_track']['uri'], state['position']), open('cache/last.p', 'wb+'))            
        
        elif command == 'auto-dj':
            self.rec = self.recs()
            self.sp.start_playback(device_id=self.device_id, uris=[self.rec])
            return {"features": self.sp.audio_features(self.rec)}

        elif command == 'device_ready':

            self.device_id = str(request.get_data().decode())

            for dev in self.sp.devices()['devices']:
                print(dev['name'])

                if dev['name'] == 'Goodify':
                    self.device_id = dev['id']
            try:

                try:
                    self.last = pickle.load(open('cache/last.p', 'rb+'))
                    self.sp.start_playback(device_id=self.device_id, uris=[self.last[0]], position_ms=self.last[1])
                except:
                    self.rec = self.recs()
                    self.sp.start_playback(device_id=self.device_id, uris=[self.rec])
            except: 
                print('could not transerfer playback automaticly :/')
    
    def recs(self):
        artists = []
        tracks = []
        formula = ''
        for x in range(4):
            artists.append(self.top_artists[random.randint(0, len(self.top_artists)-1)]['uri'])

        for x in range(4):
            tint = random.randint(0, len(self.top_tracks)-1)
            tracks.append(self.top_tracks[tint]['uri'])
            formula += self.top_tracks[tint]['name']+' + '

        recomends = self.sp.recommendations(seed_tracks=tracks, limit=100)['tracks'].pop(random.randint(0, 99))

        formula += ' = '+recomends['name']
        pickle.dump(recomends['uri'], open('cache/rec.p', 'wb+'))
        return recomends['uri']
