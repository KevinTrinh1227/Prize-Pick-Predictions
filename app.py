from flask import Flask, render_template
import json

app = Flask(__name__)

# Load the JSON file
with open('json files/recommendations.json', 'r') as f:
    data = json.load(f)

@app.route('/')
def index():
    # Render the index template and pass the player data
    return render_template('index.html', players=data)

@app.route('/static/css/styles.css')
def css():
    return app.send_static_file('css/styles.css')

if __name__ == '__main__':
    app.run(debug=True)
