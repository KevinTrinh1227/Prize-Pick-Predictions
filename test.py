import requests

# Retrieve all teams from API
url = 'https://www.balldontlie.io/api/v1/teams'
response = requests.get(url)

if response.status_code == 200:
    teams = response.json()['data']
    team_abbrs = [team['abbreviation'] for team in teams]

    # Prompt user for team abbreviation and search for matching team
    team_abbr = input("Enter team abbreviation (e.g. GSW): ").upper()
    if team_abbr in team_abbrs:
        team = teams[team_abbrs.index(team_abbr)]
        print(f"Team name: {team['full_name']}")
        print(f"Team ID: {team['id']}")
        print(f"City: {team['city']}")
    else:
        print(f"No team found with abbreviation {team_abbr}")
else:
    print('Error: HTTP Status Code', response.status_code)
