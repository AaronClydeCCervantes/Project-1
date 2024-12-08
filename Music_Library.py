from Track import Track

class MusicLibrary:
    def __init__(self):
        self.tracks = []

    def add_track(self, track):
        """Adds a track to the library, ensuring no duplicates."""
        if self.duplicate(track):
            return(f'Track {track.title} by {track.artist} is already in the library.')
        self.tracks.append(track)
        self.sort_tracks()  # Sort tracks explicitly
        return(f"Track {track.title} by {track.artist} added to the library.")

    def get_tracks(self):
        """Returns the list of tracks."""
        return self.tracks

    def display_tracks(self):
        """Displays all tracks in the library."""
        if not self.tracks:
            return 'No tracks in the library.'
        track_list = '\n'.join(
            f'[{i+1}] {self.tracks[i]}' for i in range(len(self.tracks))
        )
        return f'Music Library:\n{track_list}'
    
    def duplicate(self, newtrack):
        #checks if the track already exists in the library.
        for track in self.tracks:
            if (track.title.lower() == newtrack.title.lower() and
                track.album.lower() == newtrack.album.lower() and
                track.artist.lower() == newtrack.artist.lower()):
                return True
        return False
    
    def search_track(self, title=None, artist=None, album=None):
        """Search for a track by title."""
        matches = [
            track for track in self.tracks
            if (title and title.lower() in track.title.lower()) or
                (artist and artist.lower() in track.artist.lower()) or
                (album and album.lower() in track.album.lower())
        ]
        if not matches:
            return []
        
        return [f"{str(track)}" for track in matches]  

    def sort_tracks(self):
        """Sort tracks in the library by title."""
        self.tracks.sort(key=self.get_sort_key)

    def get_sort_key(self, track):
        """Sort key function for tracks."""
        return track.title.lower(), track.artist.lower(), track.album.lower()  # sorting by title, artist, and album
    