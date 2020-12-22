from flask import Flask, render_template, send_file, redirect, request
import subprocess, pickle, requests

app = Flask(__name__)
client_id = 'd9f97736297e4a039202cb31e162c0ef'
client_secret = '50575c7c28be4b03863f6781d0c5ad46'
response_type = 'code'
redirect_uri = 'http%3A%2F%2Flocalhost%3A5000%2Fcallback'
scope = 'user-read-private%20user-read-email'
user_token = ''
browser = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

@app.route('/')
def login():

    try:
        user_token = pickle.load(open('user_token.p', 'rb'))
    except:
        subprocess.run([
            "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type={response_type}&redirect_uri={redirect_uri}&scope={scope}"
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
    user_token = request.args.get('code')

    pickle.dump(user_token, open('user_token.p', 'wb+'))

    return 'Token was sucsesfully saved, you may close this tab :)'

print(__name__)
if __name__ == '__main__':

    #open the page in firefox
    # subprocess.run([
    #     browser,
    #     "localhost:5000"
    # ])

    app.run(debug=True)