from flask import Flask, render_template, send_file
from os import system

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/JavaScript/<string:script>')
def scripts(script):
    return send_file(f'JavaScript/{script}', mimetype="text/javascript")

@app.route('/pictures/<string:picture>')
def pictures(picture):
    print('fuck')
    return send_file(f'pictures/{picture}', mimetype='image/gif')

print(__name__)
if __name__ == '__main__':
    system('"C:\\Program Files\\Mozilla Firefox\\firefox.exe" -private-window localhost:5000')
    app.run(debug=True)