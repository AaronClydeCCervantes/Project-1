from Track import Track

class Playlist:
    def __init__(self, name):
        self.name = name
        self.tracks = []

    def add_track(self, track):
        """Add a track to the playlist."""
        if track not in self.tracks:
            self.tracks.append(track)
            return f"Track '{track.title}' added to playlist '{self.name}'."
        else:
            return f"Track '{track.title}' is already in the playlist."

    def remove_track(self, track_title):
        """Remove a track from the playlist by its title."""
        for track in self.tracks:
            if track.title == track_title:
                self.tracks.remove(track)
                return f"Track '{track_title}' removed from playlist '{self.name}'."
        return f"Track '{track_title}' not found in playlist '{self.name}'."

    def display_playlist(self):
        """Display the tracks in the playlist."""
        if not self.tracks:
            return f"Playlist '{self.name}' is empty."

        output = [f"Playlist: {self.name} ({len(self.tracks)} tracks)"]
        index = 1  # Manual index
        for track in self.tracks:
            output.append(f"[{index}]. {track.title} – {track.artist} ({track.duration})")
            index += 1
        return "\n".join(output)

    def search_track(self, title):
        """Search for a track in the playlist by title."""
        found_tracks = [track for track in self.tracks if title.lower() in track.title.lower()]
        if found_tracks:
            output = [f"Found {len(found_tracks)} track(s) in playlist '{self.name}':"]
            for track in found_tracks:
                output.append(f"- {track.title} by {track.artist}")
            return "\n".join(output)
        else:
            return f"No tracks found with title containing '{title}' in playlist '{self.name}'."

    def display_tracks(self):
        """Display detailed track information."""
        if self.tracks:
            output = [f"\nTracks in '{self.name}':"]
            index = 1  # Manual index
            for track in self.tracks:
                output.append(f"{index}. {track.title} by {track.artist} (Album: {track.album})")
                index += 1
            return "\n".join(output)
        else:
            return f"The playlist '{self.name}' has no tracks."

    def total_duration(self):
        """Calculate and return the total duration of the playlist."""
        total_seconds = sum(track.duration_seconds() for track in self.tracks)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours} hr {minutes} min {seconds} sec"
