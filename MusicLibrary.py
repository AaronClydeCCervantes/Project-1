from Track import Track

class MusicLibrary:
    def __init__(self):
        self.tracks = []
    
    def add_track(self, track):
        if self.duplicate(track):
            return "Track already exist."
        else:
            self.tracks.append(track)
            self.tracks.sort(key=Track.sort)

    def duplicate(self, new_track):
        for track in self.tracks:
            if (track.title == new_track.title and
                track.album == new_track.album and
                track.artist == new_track.artist):
                return True
            return False
     
    def display_tracks(self):
        if not self.tracks:
            return('No tracks in the library.')
        else:
            for i, track in enumerate(self.tracks):
                return(f"[{i + 1}] {track}")
    
    def search_track(self, title):
        if not title:
            return []
        else:
            return [track for track in self.tracks if title.lower() in track.title.lower()]
        
    def validate_duration(self, duration):
        try:
            mins, seconds = map(int, duration.split(':'))
            return mins >= 0 and 0 <= seconds < 60
        except ValueError:
            return False

