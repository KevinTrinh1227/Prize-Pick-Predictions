"""
    Project name: Prize Pick Predictions
    Author: Kevin Huy Trinh
    Date created: March 2022
    Python Version: 3.11.1
    Description: Linear regression python program that makes
        recommendations on betting in favor/against a player's prize
        pick line_score value using numerous machine learning algorithms. 
"""

# api link --> https://api.prizepicks.com/projections?league_id=7

import json
from tabulate import tabulate
from find_player import get_player_stats
from recommendation import predict
import time

pre_json = "pre_formatted_projections.json"  # where we copied and paste api into
post_json = "post_formatted_projections.json"  # after it gets cleaned up & formatted

# reads the pre_formmatted json file
with open(pre_json, "r") as file:
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

# lengths and member counts
num_players = len(data)
players_printed = 0

table = [] # table were printing out
n_a = "--"

with open('data.json', 'r') as f:
    existing_data = [] # the json file were saving into

for idx, key in enumerate(data):
    # the attribute values
    name = data[key]['name']
    team_name = data[key]['attributes']['team_name']
    team_city_state = data[key]['attributes']['market']

    # initialize values to "--" which is N/A
    points = n_a
    rebounds = n_a
    assists = n_a
    turnovers = n_a
    points_assists = n_a
    points_rebounds = n_a
    points_rebounds_assists = n_a

    # check if player has stat_type and update value accordingly
    for item in data[key]['strike_values']:
        if item['stat_type'] == 'Points':
            points = item['line_score']
        elif item['stat_type'] == 'Turnovers':
            turnovers = item['line_score']
        elif item['stat_type'] == 'Rebounds':
            rebounds = item['line_score']
        elif item['stat_type'] == 'Assists':
            assists = item['line_score']
        elif item['stat_type'] == 'Pts+Asts':
            points_assists = item['line_score']
        elif item['stat_type'] == 'Pts+Rebs':
            points_rebounds = item['line_score']
        elif item['stat_type'] == 'Pts+Rebs+Asts':
            points_rebounds_assists = item['line_score']

    try:
        player_name = name
        fp_player_stats, fp_player_id, fp_team_name, fp_points, fp_rebounds, fp_assists, fp_ftm, fp_points_rebounds, fp_points_assists, fp_points_rebounds_assists = get_player_stats(
            player_name)

        # making the recommendations on points
        recommendation_pts = predict(points, fp_points, n_a)
        recommendation_reb = predict(rebounds, fp_rebounds, n_a)
        recommendation_ast = predict(assists, fp_assists, n_a)

        # findind the combined stats
        recommendation_pts_ast = predict(points_assists, fp_points + fp_assists, n_a)
        recommendation_pts_reb = predict(points_rebounds, fp_points + fp_assists, n_a)
        recommendation_pts_ast_reb = predict(points_rebounds_assists, fp_points + fp_assists + fp_rebounds, n_a)


        table.append([idx + 1, name, team_name, points, fp_points, recommendation_pts, rebounds, fp_rebounds, recommendation_reb, assists, fp_assists, recommendation_ast, points_assists,
                      points_rebounds, points_rebounds_assists])


        # Append current player to the data list
        existing_data.append({
            "name": name,
            "team_name": team_name,
            "points": points,
            "fp_points": fp_points,
            "recommendation_pts": recommendation_pts,
            "diff_pts": abs(fp_points - points),
            "rebounds": rebounds,
            "fp_rebounds": fp_rebounds,
            "recommendation_reb": recommendation_reb,
            "diff_reb": abs(fp_rebounds - rebounds),
            "assists": assists,
            "fp_assists": fp_assists,
            "recommendation_ast": recommendation_ast,
            "diff_assists": abs(fp_assists - assists),
            "points_assists": points_assists,
            "fp_points_assists": fp_points + fp_assists,
            "recommendation_pts_ast": recommendation_pts_ast,
            "points_rebounds": points_rebounds,
            "fp_points_rebounds": fp_points + fp_rebounds,
            "recommendation_pts_reb": recommendation_pts_reb,
            "points_rebounds_assists": points_rebounds_assists,
            "fp_points_rebounds_assists": fp_points + fp_assists + fp_rebounds,
            "recommendation_pts_ast_reb": recommendation_pts_ast_reb
        })

        # Save data to a JSON file, overwriting any existing data
        with open('data.json', 'w') as f:
            json.dump(existing_data, f, indent=2)

        time.sleep(1)  # to avoid being rate limited
    except Exception as e:
        player_name = name
        print(f"Failed to find {player_name}. Exception: {e}. Now skipping.")

    players_printed += 1
    print(f"{players_printed}/{num_players} players have been loaded. ({round((players_printed/num_players) * 100)}%)")

# number of players with atleast 1 missing stat
num_na_stats = sum(1 for row in table if n_a in row)

print(tabulate(table,
               headers=['##', 'Name', 'Team Name', 'Pts', "FP-Pts", "Bet Rec.", "Rebs", "FP_reb", "Bet Rec.", "Ast", "FP-Ast", "Bet Rec.", "Pts+Ast", "Pts+Rebs",
                        "Pts+Rebs+Ast"], tablefmt='orgtbl') + "\n")

print(f"\n{num_na_stats} players have at least one missing stat.")
print(f"A total of {num_players} player objects in json file.")
print(f"{players_printed}/{num_players} were printed out in table format.\n\n")
