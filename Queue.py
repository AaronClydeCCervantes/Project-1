import random
from Track import Track
import json

class Queue:
    def __init__(self):
        self.list = []
        self.current = None
        self.shuffle = False
        self.repeat = False
        self.pagination = 10
        self.total_duration = 0
        self.current_index = None  

    def play(self):
        if self.shuffle:
            shuffled_queue = random.sample(self.list, len(self.list))  
            self.current_index = 0  
            self.current = shuffled_queue[self.current_index]
            return f"Playing: {self.current.title}" 
        elif self.current_index is None:
            return f"No track is currently playing."
        else:
            self.current = self.list[self.current_index] 
            return f"Playing: {self.current.title}" 

    def skip(self):
        if self.current_index is None:
            return f"No track is currently playing."
        
        if self.current_index + 1 < len(self.list):
            self.current_index += 1
            self.current = self.list[self.current_index]  
            return f"Playing: {self.current.title}"  
        elif self.repeat:
            self.current_index = 0
            self.current = self.list[self.current_index] 
            return f"Playing: {self.current.title}"
        else:
            return f"End of the queue."
        
    def previous(self):
        if self.current_index is None:
            return f"No track is currently playing."
        
        if self.current_index - 1 >= 0:
            self.current_index -= 1
            self.current = self.list[self.current_index]  
            return f"Playing: {self.current.title}"  
        else:
            return f"No previous track. You are at the start of the queue."
        
    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        status = "enabled" if self.shuffle else "disabled"
        return f"Shuffle is now {status}."
    
    def add_tracks(self, new_tracks):
        for track in new_tracks:
            self.list.append(track)
        if not self.current:
            self.current = self.list[0]
            self.current_index = 0
        self.total_duration

        return f"Added {len(new_tracks)} tracks to the queue."

    def display_queue(self, page_number=1):
        if not self.list:
            return "The queue is empty."

        total_pages = (len(self.list) + self.pagination - 1) // self.pagination
        page_number = max(1, min(page_number, total_pages))

        total_duration = sum(track.duration for track in self.list)

        print(f"Total Duration: {total_duration // 3600} hr {total_duration % 3600 // 60} min {total_duration % 60} sec")
        print(f"Shuffle: {'On' if self.shuffle else 'Off'} | Repeat: {'On' if self.repeat else 'Off'}")
        print(f"Page {page_number} of {total_pages}")
        print("Tracks:")

        start = (page_number - 1) * self.pagination
        end = min(start + self.pagination, len(self.list))
        for i in range(start, end):
            prefix = "(Currently Playing)" if i == self.current_index else f"({i + 1})"
            track = self.list[i]
            print(f"{prefix} {track.title} - {track.artist} ({self._format_duration(track.duration)})")

    def next_page(self, current_page):
        """Navigate to the next page."""
        total_pages = (len(self.list) + self.pagination - 1) // self.pagination
        next_page = current_page + 1 if current_page < total_pages else total_pages
        self.display_queue(next_page)

    def previous_page(self, current_page):
        """Navigate to the previous page."""
        prev_page = current_page - 1 if current_page > 1 else 1
        self.display_queue(prev_page)

    def queue_navigation(self):
        """Manage queue navigation within the Queue class."""
        page_number = 1
        while True:
            self.display_queue(page_number)  # Use Queue's display method directly

            print("\nQueue Navigation:")
            print(f"1. Next Page")
            print(f"2. Previous Page")
            print(f"3. Go Back to Main Menu")

            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    page_number += 1
                    self.next_page(page_number)  # Use Queue's method for next page
                elif choice == 2:
                    page_number -= 1
                    self.previous_page(page_number)  # Use Queue's method for previous page
                elif choice == 3:
                    break  # Go back to the main menu
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def _format_duration(self, duration):
        """Helper to format duration in seconds as mm:ss."""
        minutes = duration // 60
        seconds = duration % 60
        return f"{minutes}:{seconds:02}"

    def save_queue(self):
        try:
            with open("queues.json", "r") as file:
                existing_tracks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_tracks = []

        existing_titles = {track['title'] for track in existing_tracks}
        current_tracks = [
            {
                "title": track.title,
                "artist": track.artist,
                "album": track.album,
                "duration": track.duration,
            }
            for track in self.list if track.title not in existing_titles
        ]

        existing_tracks.extend(current_tracks)

        with open("queues.json", "w") as file:
            json.dump(existing_tracks, file, indent=4)

        print("Queue saved.")

    def load_queue(self):
        try:
            with open("queues.json", "r") as file:
                tracks = json.load(file)

            self.list = [
                Track(track["title"], track["artist"], track["album"], track["duration"])
                for track in tracks
                if isinstance(track, dict) and all(key in track for key in ["title", "artist", "album", "duration"])
            ]
            self.total_duration = sum(track.duration for track in self.list)
            self.current_index = 0 if self.list else None
            print("Queue loaded.")
        except FileNotFoundError:
            print("No saved queue found.")
        except json.JSONDecodeError:
            print("Error decoding JSON. Queue file might be corrupted.")

    def exit(self):
        self.save_queue()
        print("Queues saved.")