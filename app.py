from flask import Flask, render_template

import json

app = Flask(__name__)

with open('json files/points_assists.json') as f:
    data = json.load(f)


@app.route('/')
def index():
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
