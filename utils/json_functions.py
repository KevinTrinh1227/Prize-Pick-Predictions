import os
import json

def wipe_json_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'w') as file:
                json.dump([], file)
                
# Function to handle file opening or creation
def open_or_create_json(file_path, default_data):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # Create the file if it doesn't exist
        with open(file_path, 'w') as file:
            json.dump(default_data, file)
        data = default_data
    return data