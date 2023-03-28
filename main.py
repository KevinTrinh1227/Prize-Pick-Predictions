"""
    Project name: Prize Pick Predictions
    Author: Kevin Huy Trinh
    Date created: March, 2022
    Python Version: 3.11.1
    Description: Linear regression python program that makes
        recommendations on betting in favor/against a player's prize
        pick line_score value using numerous machine learning algorithms. 
"""

#api link --> https://api.prizepicks.com/projections?league_id=7

import json
import numpy as np

pre_json = "pre_formatted_projections.json" #where we copied and paste api into
post_json = "post_formatted_projections.json" #after it gets cleaned up & formatted


# reads the pre_formmatted json file
with open(pre_json, "r") as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)
    # Format the JSON with indentation
    json_str = json.dumps(data, indent=4)
    

# pre_formmatted json --> post_formatted json
json_dict = json.loads(json_str)
with open(pre_json, "w") as file:
    json.dump(json_dict, file, indent=4)


# Create dictionary to store results
results = {}

# Loop through included data to get player names and IDs
for item in data['included']:
    if item['type'] == 'new_player':
        player_id = item['id']
        player_name = item['attributes']['name']
        results[player_id] = {
            'name': player_name,
            'strike_values': []
        }

# Loop through projection data and match player IDs to add stat_type and line_score
for projection in data['data']:
    if projection['type'] == 'projection':
        player_id = projection['relationships']['new_player']['data']['id']
        stat_type = projection['attributes']['stat_type']
        line_score = projection['attributes']['line_score']
        results[player_id]['strike_values'].append({
            'stat_type': stat_type,
            'line_score': line_score
        })
        # Add player attributes to results dictionary
        for player in data['included']:
            if player['type'] == 'new_player' and player['id'] == player_id:
                results[player_id]['attributes'] = player['attributes']

# Write results to JSON file
with open(post_json, 'w') as f:
    json.dump(results, f, indent=2)
with open(post_json, 'r') as f:
    data = json.load(f)
    
num_players = len(data)
print(f"Total number of players: {num_players}\n")
"""
for key in data:
    name = data[key]['name']
    team_name = data[key]['attributes']['team_name']
    print(name, team_name)
"""