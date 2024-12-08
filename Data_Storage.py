import json
from Music_Library import MusicLibrary
from Playlist import Playlist
from Track import Track

class DataStorage:
    @staticmethod
    def save_library(library, filepath='MusicData.json'):
        """Save music library to JSON."""
        if library is None:
            print("No library to save.")
            return
        
        data = {"Music_Library": [track.__dict__ for track in library.get_tracks()]}
        
        try:
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)  # Pretty-printing for readability
            print(f"Library saved successfully to {filepath}.")
        except Exception as e:
            print(f"Error saving library: {e}")

    @staticmethod
    def save_playlists(playlists, filepath='Playlists.json'):
        """Save playlists to JSON."""
        if playlists is None:
            print("No playlists to save.")
            return
        
        data = {"Playlists": {playlist.name: [track.__dict__ for track in playlist.tracks] for playlist in playlists}}
        
        try:
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)  # Pretty-printing for readability
            print(f"Playlists saved successfully to {filepath}.")
        except Exception as e:
            print(f"Error saving playlists: {e}")

    @staticmethod
    def load_library(filepath='MusicData.json'):
        """Load music library from JSON."""
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)

            library = MusicLibrary()

            # Load library tracks
            if "Music_Library" in data:
                for track_data in data["Music_Library"]:
                    try:
                        duration = track_data["duration"]
                        if isinstance(duration, str) and ":" in duration:  # If duration is in MM:SS format
                            minutes, seconds = map(int, duration.split(":"))
                            duration = minutes * 60 + seconds  # Convert to seconds

                        track = Track(
                            title=track_data["title"],
                            artist=track_data["artist"],
                            album=track_data["album"],
                            duration=duration
                        )
                        library.add_track(track)
                    except (ValueError, KeyError) as e:
                        print(f"Skipping invalid track data: {track_data} - Error: {e}")

            return library

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Library data not found or corrupted. Error: {e} - Initializing new library.")
            return MusicLibrary()

    @staticmethod
    def load_playlists(filepath='Playlists.json'):
        """Load playlists from JSON."""
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)

            playlists = []

            if "Playlists" in data:
                for playlist_name, track_data_list in data["Playlists"].items():
                    playlist = Playlist(playlist_name)
                    for track_data in track_data_list:
                        try:
                            duration = track_data["duration"]
                            if isinstance(duration, str) and ":" in duration:  # If duration is in MM:SS format
                                minutes, seconds = map(int, duration.split(":"))
                                duration = minutes * 60 + seconds  # Convert to seconds

                            track = Track(
                                title=track_data["title"],
                                artist=track_data["artist"],
                                album=track_data["album"],
                                duration=duration
                            )
                            playlist.add_track(track)
                        except (ValueError, KeyError) as e:
                            print(f"Skipping invalid track data in playlist '{playlist_name}': {track_data} - Error: {e}")
                    playlists.append(playlist)

            return playlists

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Playlists data not found or corrupted. Error: {e} - Initializing new playlists.")
            return []
