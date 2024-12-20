class Track:
    def __init__(self, title, artist, album, duration, additional_artist=None):
        """
        Initializes a new Track object.

        :param title: The title of the track
        :param artist: The main artist of the track
        :param album: The album the track belongs to
        :param duration: The duration of the track in "mm:ss" format
        :param additional_artist: Optional; Additional artists featured on the track (can be a string or list)
        """
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.additional_artist = (
            [additional_artist] if isinstance(additional_artist, str) else additional_artist or []
        )

    def getTitle(self):
        return self.title
    
    def getArtist(self):
        return self.artist
    
    def getAlbum(self):
        return self.album
    
    def getAdditionalArtist(self):
        return self.additional_artist
        
    def getDuration(self):
        #returns the duration of the track in seconds.
        if not self._is_validDuration():
            return 'Invalid duration format. Please use mm:ss.'
        parts = self.duration.split(':')
        mins = int(parts[0])
        seconds = int(parts[1])
        return mins * 60 + seconds

    def getDurationstr(self):
        #returns the duration of the track as a formatted string (mm:ss).
        total_seconds = self.getDuration()
        if total_seconds == -1:
            return "00:00" # default for invalid duration
        mins = total_seconds // 60
        seconds = total_seconds % 60
        return f'{mins:02}:{seconds:02}'
    
    @staticmethod
    def _is_validDuration(duration):
        #validates the duration of the format
        if not duration or ':' not in duration:
            return False
        parts = duration.split(':')
        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
            return False
        seconds = int(parts[1])
        return 0 <= seconds <= 59 
    
    def sort_key(self):
        """Sorting key for tracks by title, artist, album, and duration."""
        return self.title.lower(), self.artist.lower(), self.album.lower(), self.duration
    

    def create_track(library):
        #creates track and added it to the library
        title = input('Enter track title: ').strip()
        artist = input('Enter artist: ').strip()
        album = input('Enter album: ').strip()
        duration = input('Enter duration (mm:ss): ').strip()
        
        if not Track._is_validDuration(duration):
            return "Invalid duration format. Please enter duration in mm:ss format."

        additional_artist_input = input('Enter additional artist(s) (if more than 1 additional artist separate by comma or Enter to Skip): ').strip()
        additional_artist = [artist.strip() for artist in additional_artist_input.split(',')] if additional_artist_input else []

        new_track = Track(title, artist, album, duration, additional_artist)
        return library.add_track(new_track)
         
    def __str__(self):
    # Returns a string representation of the track.
        if self.additional_artist:
            additional = ", ".join(self.additional_artist)
            return (f"Title: {self.title}, Artist: {self.artist} feat. {additional}, "
                    f"Album: {self.album}, Duration: {self.duration}")
        else:
            return (f"Title: {self.title}, Artist: {self.artist}, "
                    f"Album: {self.album}, Duration: {self.duration}")


    def __eq__(self, other):
        """Equality comparison based on title, artist, album, and duration."""
        if not isinstance(other, Track):
            return False
        return self.sort_key() == other.sort_key()

    def __hash__(self):
        """Hashing method to allow using Track objects in sets and dictionaries."""
        return hash(self.sort_key())
    
    
