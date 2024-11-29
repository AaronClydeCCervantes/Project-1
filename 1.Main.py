# MENUS dictionary 
from MusicLibrary import MusicLibrary
from Track import Track

MENUS = {
    "main": {
        1: "Music Library",
        2: "Playlists",
        3: "Exit"
    },
    "Music library": {
        1: "Add Track",
        2: "View Tracks",
        3: "Search Tracks",
        4: "Go back to main menu"
    },
    "playlist": {
        1: "Create Playlist",
        2: "View Playlists",
        3: "Add Track to Playlist",
        4: "View Playlist",
        5: "Go back to main menu"
    },
}

def input_track(self):
    title = input('Enter a track title: ').strip()
    while not title:
        print('Track title cannot be empty.')
        title = input('Enter a track title: ').strip()
        
    artist = input('Enter artist name: ').strip()
    while not artist:
        print('Artist name cannot be empty.')
        artist = input('Enter artist name: ').strip()

    album = input('Enter album name: ').strip()
    while not album:
        print('Album name cannot be empty.')
        album = input('Enter album name: ').strip()

    duration = input('Enter track duration (MM:SS): ').strip()
    while not self.validate_duration(duration):
        print('Invalid duration format. Please enter in MM:SS format.')
        duration = input('Enter track duration (MM:SS): ').strip()

    additional_artist = input('Enter additional artists (separate with comma or leave blank): ').strip()
    additional_artist = [artist.strip() for artist in additional_artist.split(',')] if additional_artist else []

    new_track = Track(title, artist, album, duration, additional_artist)
    self.add_track(new_track)
    # print(f'Track {title} by {artist} added successfully!')

def display_tracks(library):
     print('\nAll Tracks\n')
     for track in library.tracks:
         print(track)
         
def search_track(library):
    search_title = input('Enter a title: ').strip()
    while not search_title:
        print('Search title cannot be empty.')
        search_title = input('Enter a title: ').strip()

    results = library.search_tracks(search_title)
    if results:
        print(f"\nTracks matching '{search_title}':")
        for track in results:
            print(track)
    else:
        print(f'No track found.')


def mainMenu():
    library = MusicLibrary()

    while True:
        print('\nMain Menu')
        for key, value in MENUS['main'].items():
            print(f'{key}. {value}')
        choice = input('Choose an option: ').strip()

        if choice == '1':
            while True:
                print("\nMusic Library Menu:")
                for key, value in MENUS['Music library'].items():
                    print(f"{key}. {value}")
                sub_choice = input("Choose an option: ").strip()

                if sub_choice == "1":  
                    input_track(library)
                elif sub_choice == "2":  
                    display_tracks(library)
                elif sub_choice == "3": 
                    search_track(library)
                elif sub_choice == "4": 
                    break
                else:
                    print("Invalid option. Please try again.")
        
        elif choice == "2":  
            print("Playlists")
        elif choice == "3": 
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    mainMenu()
                