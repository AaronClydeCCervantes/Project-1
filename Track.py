class Track:
    def __init__(self, title, artist, album, duration, additional_artist):
        """
        Initializes a new Track object.

        :param title: The title of the track
        :param artist: The artist of the track
        :param album: The album of the track
        :param duration: The duration of the track in "mm:ss" format
        """
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.additional_artist = [additional_artist] if isinstance(additional_artist, str) else additional_artist or []

    def getDuration(self):
        mins, seconds = int(self.duration.split(':')[0]), int(self.duration.split(':')[1])
        return mins * 60 + seconds

    def getDurationstr(self):
        total_seconds = self.getDuration()
        mins = total_seconds // 60
        seconds = total_seconds % 60
        return f'{mins:02}:{seconds:02}'
    
    def sort(self):
        return self.title.lower(), self.artist.lower(), self.album.lower(), self.duration

    def __str__(self):
        add = ", ".join(self.additional_artist) if self.additional_artist else 'No additional artists'
        return f'Title: {self.title}\nArtist: {self.artist}\nAlbum: {self.album}\nDuration: {self.duration}\nAdditional Artist: {add}\n'
        