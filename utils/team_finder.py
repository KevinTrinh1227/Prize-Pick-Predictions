""" =============================================
* finds the nba team given the abbreviation and
* calculates the team's elo.
============================================= """

import requests

def get_team_info(team_abbreviation):
    
    api_url = "https://www.balldontlie.io/api/v1/teams"

    
    response = requests.get(api_url)

    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the data contains any teams from the balldontlie api
        if data.get("data"):
            teams = data["data"]

            for team in teams:
                if team["abbreviation"] == team_abbreviation:
                    city = team.get("city", "N/A")
                    name = team.get("full_name", "N/A")
                    team_id = team.get("id", "N/A")

                    return {
                        "City": city,
                        "Name": name,
                        "ID": team_id
                    }

            # If no matching team was found
            return {"error": "Team not found"}
        else:
            return {"error": "No teams found in the API response"}
    else:
        return {"error": f"Failed to retrieve data. Status code: {response.status_code}"}


# ex usage
team_abbreviation = "LAL"
result = get_team_info(team_abbreviation)

if "error" in result:
    print(result["error"])
else:
    print("City:", result["City"])
    print("Name:", result["Name"])
    print("ID:", result["ID"])
