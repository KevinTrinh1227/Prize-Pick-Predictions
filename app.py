from flask import Flask, render_template, request
import json

app = Flask(__name__)

# points.json is default when loading up
with open('json files/points.json') as f:
    data = json.load(f)

# Route for the home page
@app.route('/')
def index():

    """ =============================================
    * Check if a data source parameter was passed in the URL
    * This allows the user to switch between json files
    * to view the recommendations for different stat types
    ============================================= """
    data_source = request.args.get('data_source', 'points')
    if data_source == 'points':
        with open('json files/points.json') as f:
            data = json.load(f)
    elif data_source == 'rebounds':
        with open('json files/rebounds.json') as f:
            data = json.load(f)
    elif data_source == 'assists':
        with open('json files/assists.json') as f:
            data = json.load(f)
    elif data_source == 'pts_asts':
        with open('json files/points_assists.json') as f:
            data = json.load(f)
    elif data_source == 'pts_rebs':
        with open('json files/points_rebounds.json') as f:
            data = json.load(f)
    elif data_source == 'pts_rebs_asts':
        with open('json files/points_assists_rebounds.json') as f:
            data = json.load(f)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()