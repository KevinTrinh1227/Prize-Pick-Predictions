from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

with open('json files/recommendations.json') as f:
    data = json.load(f)

@app.route('/')
def index():
    players = []
    for player in data:
        player_data = list(player.values())[0]
        player_name = list(player.keys())[0]
        player_image = player_data['general']['picture_link']
        players.append({'name': player_name, 'image': player_image})
    return render_template('index.html', players=players)

if __name__ == '__main__':
    app.run()
