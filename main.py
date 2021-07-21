from flask import Flask, render_template, send_file, redirect, request
from flask_restful import Api, Resource
import subprocess, pickle, requests, base64, spotipy, json, random
from spotipy import util
from selenium import webdriver
import userData

from API import Resources

app = Flask(__name__)
api = Api(app)

api.add_resource(Resources, '/API/<string:command>')

# sp = spotipy()

# driver = webdriver.Firefox()

client_id = 'not for u'
client_secret = 'not for u'
response_type = 'code'
redirect_uri = 'http://localhost:5000/callback'
scope = 'streaming,user-read-playback-state,user-modify-playback-state,user-read-recently-played,user-top-read,user-read-playback-position,playlist-modify-private'
user_data = None
sp = None
Token = None
browser = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

@app.route('/')
def login():

    Token = util.prompt_for_user_token(
            'Q',
            scope,
            client_id=client_id ,
            client_secret=client_secret,
            redirect_uri='https://www.google.com/'
    )

    sp = spotipy.Spotify(auth=Token)

    return redirect('/index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/main.css')
def css():
    return send_file(f'templates/main.css', mimetype="text/stylesheet")

@app.route('/JavaScript/<string:script>')
def scripts(script):
    return send_file(f'JavaScript/{script}', mimetype="text/javascript")

@app.route('/pictures/<string:picture>')
def pictures(picture):
    return send_file(f'pictures/{picture}', mimetype='image/gif')

@app.route('/shaders/<string:shader>')
def shaders(shader):
    return send_file(f'shaders/{shader}', mimetype='text/glslCanvas')

@app.route('/callback')
def callback():

    user_data = userData.userData()

    user_data.user_key = request.args.get('code')

    #get token and refresh

    encoded_ids = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ascii")).decode('ascii')

    spotify_request_result = requests.post(
        'https://accounts.spotify.com/api/token',
        
        data = {'Content-Type':'application/x-www-form-urlencoded', 
                  'grant_type':'authorization_code', 
                  'code':user_data.user_key, 
                  'redirect_uri':redirect_uri},

        headers = {'Authorization':f'Basic {encoded_ids}'}
                
    )

    if spotify_request_result.status_code == 200:

        #save user data

        user_data.user_token = spotify_request_result.json()['access_token']
        user_data.user_refresh = spotify_request_result.json()['refresh_token']
        user_data.scope = spotify_request_result.json()['scope']

        pickle.dump(user_data, open('user_data.p', 'wb+'))
        return 'Token was sucsesfully saved, you may close this tab :)'

    else:
        print(spotify_request_result.json)
        return spotify_request_result.text

print(__name__)
if __name__ == '__main__':

    app.run(debug=False)

    # driver.get('http://127.0.0.1:5000/')