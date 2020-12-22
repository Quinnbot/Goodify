from flask import Flask, render_template, send_file, redirect, request
import subprocess, pickle, requests, base64, json
import userData

app = Flask(__name__)
client_id = 'd9f97736297e4a039202cb31e162c0ef'
client_secret = '50575c7c28be4b03863f6781d0c5ad46'
response_type = 'code'
redirect_uri = 'http://localhost:5000/callback'
scope = 'user-read-private%20user-read-email'
user_data = None
browser = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

@app.route('/')
def login():

    try:
        user_data = pickle.load(open('user_data.p', 'rb'))
    except:
        subprocess.run([
            "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type={response_type}&redirect_uri={redirect_uri.replace('/', '%2F').replace(':', '%3A')}&scope={scope}"
        ])

    return redirect('/index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/JavaScript/<string:script>')
def scripts(script):
    return send_file(f'JavaScript/{script}', mimetype="text/javascript")

@app.route('/pictures/<string:picture>')
def pictures(picture):
    return send_file(f'pictures/{picture}', mimetype='image/gif')

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

    #open the page in firefox
    # subprocess.run([
    #     browser,
    #     "localhost:5000"
    # ])

    app.run(debug=True)