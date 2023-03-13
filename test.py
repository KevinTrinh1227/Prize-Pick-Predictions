import requests
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Define the player ID and API endpoint
player_id = 61
endpoint = f"https://www.balldontlie.io/api/v1/stats?seasons[]=2022&per_page=100&player_ids[]={player_id}"

# Retrieve the data from the API
response = requests.get(endpoint)
data = response.json()

# Extract the features and labels from the data
features = []
labels = []
for game in data["data"]:
    stats = game["stats"]
    for stat in stats:
        if stat["player_id"] == player_id:
            stat_type = stat["stat_type"]
            line_score = stat["line_score"]
            value = stat["value"]
            features.append([value])
            labels.append(line_score)

# Convert the features and labels to numpy arrays
X = np.array(features)
y = np.array(labels)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the linear regression model on the training set
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model's performance on the testing set
score = model.score(X_test, y_test)
print(f"R-squared score: {score:.3f}")

# Predict whether the player will make lower or higher than their "line_score"
predictions = []
for feature in X_test:
    prediction = model.predict([feature])
    if prediction < y.mean():
        predictions.append("lower")
    else:
        predictions.append("higher")

# Print the predictions for each stat type
stat_types = ["Blocked Shots", "Pts+Rebs", "Points", "Rebs+Asts", "Pts+Asts", "Free Throws Made", "Pts+Rebs+Asts", "Rebounds", "Assists"]
for i, prediction in enumerate(predictions):
    print(f"{stat_types[i]}: {prediction}")
