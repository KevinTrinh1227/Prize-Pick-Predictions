import json
from flask import Flask, render_template

# Step 1: Load the JSON file and store it in a Python dictionary
with open('json files/recommendations.json') as f:
    player_stats = json.load(f)

# Step 2: Create a Flask app and define the routes
app = Flask(__name__)

# Home page with the 6 buttons
@app.route('/')
def home():
    return render_template('home.html')

# Endpoint to retrieve the player stats for a specific category
@app.route('/stats/<category>')
def get_player_stats(category):
    # Step 4: Write a function to extract the data for a specific stat
    def filter_stats(player):
        return player[category]['recommendation_' + category] != '--'

    # Filter the player stats based on the selected category
    players = {name: stats for name, stats in player_stats.items() if filter_stats(stats)}

    # Render the player stats template with the filtered data
    return render_template('player_stats.html', players=players)

if __name__ == '__main__':
    app.run(debug=True)
