import time
from flask_restful import Resource, Api, request
from spotipy import util
import pickle, spotipy, random, json, threading


class Resources(Resource):

    def __init__(self):
        self.client_id = 'not for u'
        self.client_secret = 'not for u'
        self.scope = 'streaming,user-read-playback-state,user-modify-playback-state,user-read-recently-played,user-top-read,user-read-playback-position,playlist-modify-private'
        
        self.device_id = None

        self.token = util.prompt_for_user_token(
            'Q',
            self.scope,
            client_id=self.client_id ,
            client_secret=self.client_secret,
            redirect_uri='https://www.google.com/'
        )
        self.sp = spotipy.Spotify(auth=self.token)

        self.top_artists = self.sp.current_user_top_artists()['items']
        self.top_tracks = self.sp.current_user_top_tracks()['items']
        try:
            self.rec = pickle.load(open('cache/rec.p', 'rb'))
        except:
            self.rec = None
        
    def get(self, command):

        if command == 'token':
            try:
                
                
                return {"token": self.token, "refresh": 'None'}
            except:
                return {"token": "none", "refresh": "none"}

        elif command == 'next':
            pass

        else:
            return {"command": "invalid"}

    def post(self, command):
        print(threading.active_count())

        if command == 'player_state' and threading.active_count() == 3:
            state = json.loads(request.data)
            percent = 1 - (state['position']/state['duration'])

            print('\n{} rec: {} playing: {}\n'.format(percent, self.rec, state['track_window']['current_track']['uri']))
            
            if( self.rec == None ):
                self.rec = self.recs(state)
                self.sp.add_to_queue(self.rec, device_id=self.device_id)

            if(percent == 1.0 and self.rec == state['track_window']['current_track']['uri']):
                self.rec = 'temp'
                self.rec = self.recs(state)
                print('adding {} to queue'.format(self.rec))
                self.sp.add_to_queue(self.rec, device_id=self.device_id)

                if state['duration'] >= 30000:
                    print('sleeping to check for a "listen"')
                    time.sleep(30)
                    temp_cp = self.sp.current_playback()
                    print(temp_cp['item']['uri'])


        if command == 'device_ready':

            self.device_id = str(request.get_data().decode())

            for dev in self.sp.devices()['devices']:
                print(dev['name'])

                if dev['name'] == 'Goodify':
                    self.device_id = dev['id']
            try:
                self.sp.transfer_playback(self.device_id)
            except: 
                print('could not transerfer playback automaticly :/')

    def recs(self, state):
        artists = []
        tracks = []
        formula = ''
        for x in range(4):
            artists.append(self.top_artists[random.randint(0, len(self.top_artists)-1)]['uri'])

        for x in range(4):
            tint = random.randint(0, len(self.top_tracks)-1)
            tracks.append(self.top_tracks[tint]['uri'])
            formula += self.top_tracks[tint]['name']+' + '
        
        tracks.append(state['track_window']['current_track']['uri'])
        artists.append(state['track_window']['current_track']['artists'][0]['uri'])

        recomends = self.sp.recommendations(seed_tracks=tracks, limit=100)['tracks'].pop(random.randint(0, 99))

        formula += ' = '+recomends['name']
        print(formula)
        pickle.dump(recomends['uri'], open('cache/rec.p', 'wb+'))
        return recomends['uri']
