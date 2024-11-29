
from Track import Track
import json

class Playlist:
    def __init__(self, name):
        self.name = name
        self.tracks = []  
        self.track_map = {}  
        self.total_duration = [0, 0]  

    def add_track(self, track: Track):
        """Add a unique track to the playlist."""
        if track.getTitle() not in self.track_map:
            self.tracks.append(track)
            self.track_map[track.getTitle()] = track 
            self._update_duration(track.getNumericDuration())
            return True
        return False

    def remove_track(self, track: Track):
        """Remove a track from the playlist."""
        track_title = track.getTitle()
        if track_title in self.track_map:
            self.tracks.remove(track) 
            self._update_duration(track.getNumericDuration(), remove=True)
            del self.track_map[track_title]  
            return True
        return False

    def _update_duration(self, duration, remove=False):
        """Update the total duration of the playlist."""
        minutes, seconds = self.total_duration
        delta_min, delta_sec = duration

        total_seconds = (minutes * 60) + seconds
        delta_seconds = (delta_min * 60) + delta_sec

        if remove:
            total_seconds -= delta_seconds
        else:
            total_seconds += delta_seconds

        self.total_duration[0] = total_seconds // 60
        self.total_duration[1] = total_seconds % 60

    def get_total_duration(self):
        """Return the total duration in 'mm:ss' format."""
        mins = self.total_duration[0]
        secs = self.total_duration[1]
        return f"{mins:02}:{secs:02}"


    def save_playlist(self, file_path="Playlist.json"):
      """Save the playlist to a JSON file."""
      try:
        # Load existing data if the file exists
        with open(file_path, "r") as f:
            data = json.load(f)
      except FileNotFoundError:
        # Create a new dictionary if the file doesn't exist
        data = {}

      # Update the playlist data
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

      # Save back to the JSON file
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
        # Load the data from the JSON file
        with open(file_path, "r") as f:
            data = json.load(f)
      except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return None
      except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' contains invalid JSON.")
        return None

      # Check if the playlist exists in the data
      if name in data:
        playlist_data = data[name]
        playlist = Playlist(playlist_data["Playlist Name"])

        # Deserialize tracks
        playlist.tracks = [
            Track.from_dict(track_data)
            for track_data in playlist_data.get("Tracks", [])
        ]

        # Parse total duration (stored in seconds)
        playlist.total_duration = playlist_data.get("Total Duration", 0)

        print(f"Playlist '{name}' loaded successfully.")
        return playlist
      else:
        print(f"Playlist '{name}' not found in '{file_path}'.")
        return None

    def __str__(self):
        """Return a string representation of the playlist."""
        track_list = "\n".join([str(track) for track in self.tracks])
        duration = f"{self.total_duration['minutes']} min {self.total_duration['seconds']} sec"
        return f"Playlist: {self.name}\nTotal Duration: {duration}\nTracks:\n{track_list}"