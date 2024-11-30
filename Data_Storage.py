import json
import json
from Track import Track
from Playlist import Playlist
from Music_Library import MusicLibrary
from Queue import Queue

class DataStorage:
#MUSIC Library and Playlist
    #SAVE
    def save_music(music_data):
        try:
            with open("Music_Data.json", 'w') as json_file:
                json.dump(music_data, json_file, indent=4)  
            print(f"Playlist saved successfully to Music_Data}")
        except Exception as e:
            print(f"Error saving playlist: {e}")

    #LOAD
    def load_music(self):
        try:
          
            with open("Music_Data.json", 'r') as json_file:
                playlist_data = json.load(json_file)  
            print(f"Playlist loaded successfully from Music_Data.json")
            return playlist_data  
        except FileNotFoundError:
            print(f"Error: The file Music_Data.json was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON in Music_Data.json, It might be corrupted or not properly formatted.")

    def save_playlist(self, file_path="Playlist.json"):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data[self.name] = {
            "Playlist Name": self.name,
            "Total Duration": f"{self.total_duration[0]} min {self.total_duration[1]} sec",
            "Tracks": [
                {
                    "Title": track.title,
                    "Artist": track.artist,
                    "Album": track.album,
                    "Duration": track.duration,
                }
                for track in self.tracks
            ],
        }


        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Playlist '{self.name}' saved successfully.")
        except Exception as e:
            print(f"Error saving playlist: {e}")

    @staticmethod
    def load_playlist(name, file_path="Playlist.json"):
      """Load a playlist by name from a JSON file."""
      try:
        with open(file_path, "r") as f:
            data = json.load(f)
      except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return None
      except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' contains invalid JSON.")
        return None


      if name in data:
        playlist_data = data[name]
        playlist = Playlist(playlist_data["Playlist Name"])


        playlist.tracks = [
            Track.from_dict(track_data)
            for track_data in playlist_data.get("Tracks", [])
        ]

   
        playlist.total_duration = playlist_data.get("Total Duration", 0)

        print(f"Playlist '{name}' loaded successfully.")
        return playlist
      else:
        print(f"Playlist '{name}' not found in '{file_path}'.")
        return None

#QUEUE

    def save_queue(self):
        try:
            with open("queues.json", "r") as file:
                existing_tracks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_tracks = []

        current_tracks = [
            {"title": track.title, "artist": track.artist, "duration": track.duration}
            for track in self.list
        ]
        existing_tracks.extend(current_tracks)

        with open("queues.json", "w") as file:
            json.dump(existing_tracks, file, indent=4)

        print("Queues saved.")

    def load_queue(self):
        try:
            with open("queues.json", "r") as file:
                tracks = json.load(file)

            self.list = [
                Track(track["title"], track["artist"], track["album"], track["duration"]) for track in tracks
            ]
            self.total_duration = sum(track["duration"] for track in tracks)
            self.current_index = 0 if self.list else None
            print("Queues loaded.")
        except FileNotFoundError:
            print("No saved queue found.")
        except json.JSONDecodeError:
            print("Error decoding JSON. Queue file might be corrupted.")   


    
