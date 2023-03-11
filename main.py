import json
from tabulate import tabulate

# Read JSON file
with open('league_7_projections.json') as f:
    data = json.load(f)

# Get the data for new players
new_players = [item for item in data["included"] if item["type"] == "new_player"]

# Print the total number of rows
num_rows = len(new_players)
print(f"Total rows: {num_rows}\n")

# Initialize the index counter
index = 1

# Print the table with index numbers
print("{:<8} {:<30} {:<10} {:<10} {:<10}".format("Index", "Name", "Team", "Position", "ID"))
for player in new_players:
    name = player["attributes"]["name"]
    team = player["attributes"]["team_name"]
    position = player["attributes"]["position"]
    id = player["id"]
    print("{:<8} {:<30} {:<10} {:<10} {:<10}".format(f"{index}.", name, team, position, id))
    index += 1



#print(f"\nA total of {total_players} were printed")