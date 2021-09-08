from flask import Flask, render_template, send_file, redirect, request
from flask_restful import Api, Resource
from spotipy import util
from API import Resources
import spotipy

app = Flask(__name__)
api = Api(app)

api.add_resource(Resources, '/API/<string:command>')

response_type = 'code'
scope = 'streaming,user-read-playback-state,user-modify-playback-state,user-read-recently-played,user-top-read,user-read-playback-position,playlist-modify-private'
user_data = None
sp = None
Token = None

@app.route('/')
def login():

    Token = util.prompt_for_user_token('Q', scope, redirect_uri='https://www.google.com/')

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
    sp = spotipy.Spotify(auth=request.args.get('code'))
    return ''

print(__name__)
if __name__ == '__main__':

    app.run(debug=True)