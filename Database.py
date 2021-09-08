from logging import lastResort
from numpy import add
from pandas.core.frame import DataFrame
import spotipy, pandas, pickle
from spotipy import util
from datetime import datetime

class Database:

    def __init__(self, sp: spotipy.Spotify):

        self.sp = sp

        try:
            self.plays = pickle.load( open('cache/{}-plays.p'.format('temp'), 'rb+'))
        except FileNotFoundError:
            self.plays = pandas.DataFrame(columns = ['Name', 'URI', 'Timestamp'])
            self.SaveDB()
            self.GetSpotifyHistory()
    
    def PlayedRecently(self, URI: str, Delta: int):

        now = int(datetime.now().timestamp() * 1000)

        # for row in self.plays.iterrows():
        #     if row. 

    def GetSongRecommendation(self, ):



        print('')

    def GetSpotifyHistory(self):

        
        LatestTimestamp = None

        try:
            LatestTimestamp = self.plays.sort_values(by=['Timestamp'], ascending = False)['Timestamp'][0]
        except IndexError:
            print('local history cache empty')
            LatestTimestamp = 0

        tracks = self.sp.current_user_recently_played()['items']

        for track in tracks:
            ts = int((datetime.strptime(track['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime(1970, 1, 1)).total_seconds()*1000)
            
            if ts > LatestTimestamp:
                print('ts:   {} \nnow: {}'.format(ts, LatestTimestamp))
                print('\n\nadding: {} to plays\n\n'.format(track['track']['name']))
                self.AddPlay(track['track']['name'], track['track']['uri'], ts)

        self.SaveDB()
        

    #'artist', 'album', 'track', 'playlist'
    #will check local db first
    def Search(self, Query: str, ReturnAmt: int = 1, Type: str = 'track'):
        
        results = []

        for index, row in self.plays.iterrows():
            if  str(row['Name']).lower() == Query.lower():
                results.append((row['Name'], row['URI'], row['Timestamp']))

        if results:
            return results
        else:
            SpotSearch = self.sp.search(q=Query, limit=ReturnAmt, type=Type)
            SpotSearch = SpotSearch['tracks']['items']

            for items in SpotSearch:
                results.append((items['name'], items['uri'], datetime.now().timestamp() * 1000))
            
            return results

    def SaveDB(self):

        # self.plays = self.plays.sort_values(by=['Timestamp'], ascending = False)

        pickle.dump(self.plays, open('cache/{}-plays.p'.format('temp'), 'wb+'))
    
    def AddPlay(self, Name: str, URI: str, Timestamp: int):
        newrow = pandas.DataFrame({'Name':Name, 'URI':URI, 'Timestamp':Timestamp}, index=[0])
        self.plays = pandas.concat([newrow, self.plays]).reset_index(drop=True)


if __name__ == '__main__':
    

    Token = util.prompt_for_user_token('Q')

    sp = spotipy.Spotify(auth=Token)

    test = Database(sp)

    print(test.plays.head(10))