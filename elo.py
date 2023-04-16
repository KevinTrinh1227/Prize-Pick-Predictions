import requests

# Enter the player's name and team name to look up
player_name = 'LeBron'
team_name = 'Lakers'

# Make a request to theballdontlie API to get all players on the team
response = requests.get(f'https://www.balldontlie.io/api/v1/players?per_page=100&team={team_name}')

# Iterate through each player on the team and check if their name matches the given name
for player in response.json()['data']:
    if player['first_name'] + ' ' + player['last_name'] == player_name:
        player_id = player['id']
        print(f"The player's ID is {player_id}")
        break

# If no player with the given name was found on the team, print an error message
else:
    print(f"No player named {player_name} was found on the {team_name}")
