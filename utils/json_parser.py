""" =============================================
* This module takes in two json files, and
* cleans/extracts only relevant information
* and formats it into the other json file
============================================= """

import json
def parse_json_file(pre_json, post_json):
    # reads the pre_json json file
    with open(pre_json, "r") as file:
        data = json.load(file)
        json_str = json.dumps(data, indent=2)

    # formats the messy json file
    json_dict = json.loads(json_str)
    with open(pre_json, "w") as file:
        json.dump(json_dict, file, indent=2)

    # Loop through included data to get player names and IDs
    results = {}  # Create dictionary to store results
    for item in data['included']:
        if item['type'] == 'new_player':
            player_id = item['id']
            player_name = item['attributes']['name']
            results[player_id] = {
                'name': player_name,
                'opposing_team_abv': None,  # initial value of nothing
                'strike_values': []
            }

    # Loop through projection data and match player IDs to add stat_type and line_score
    for projection in data['data']:
        if projection['type'] == 'projection':
            player_id = projection['relationships']['new_player']['data']['id']
            stat_type = projection['attributes']['stat_type']
            line_score = projection['attributes']['line_score']
            opposing_team = projection['attributes']['description']
            results[player_id]['strike_values'].append({
                'stat_type': stat_type,
                'line_score': line_score
            })
            results[player_id]['opposing_team_abv'] = opposing_team
            # Add player attributes to results dictionary
            for player in data['included']:
                if player['type'] == 'new_player' and player['id'] == player_id:
                    results[player_id]['attributes'] = player['attributes']

    # Write results to JSON file
    with open(post_json, 'w') as f:
        json.dump(results, f, indent=2)
    with open(post_json, 'r') as f:
        data = json.load(f)
    return data
