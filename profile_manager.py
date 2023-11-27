import json
import os

class ProfileManager:
    def __init__(self):
        self.profiles_file = 'profiles.json'

    def load_profiles(self):
        if os.path.exists(self.profiles_file):
            with open(self.profiles_file, 'r') as file:
                return json.load(file)
        return {}

    def save_profiles(self, profiles):
        with open(self.profiles_file, 'w') as file:
            json.dump(profiles, file)
