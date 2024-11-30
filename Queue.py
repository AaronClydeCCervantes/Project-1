import random
import json
from Track import Track

class Queue:
    def __init__(self):
        self.list = []
        self.current = None
        self.shuffle = False
        self.repeat = False
        self.pagination = 10
        self.total_duration = 0
        self.originalOrder = []
        self.current_index = None  # Initialize current_index

    def play(self):
        if self.shuffle:
            shuffled_queue = random.sample(self.list, len(self.list))
            self.current_index = 0
            print(f"Playing: {shuffled_queue[self.current_index]}")
        elif self.current_index is None:
            print("No track is currently playing.")
        else:
            print(f"Playing: {self.list[self.current_index]}")

    def skip(self):
        if self.current is None:
            print("No track is currently playing.")
            return
        
        if self.current.next is None and not self.repeat:
            print("End of the queue. No more tracks to skip to.")
            return
        
        if self.repeat:
            self.current = self.list.head.track
            print(f"Playing: {self.current}")
        else:
            self.current = self.current.next.track if self.current.next else None
            if self.current:
                print(f"Playing: {self.current}")
            else:
                print("End of the queue.")

    def previous(self):
        if self.current is None:
            print("No track is currently playing.")
            return
        
        if self.current.prev is None:
            print("No previous track. You are at the start of the queue.")
            return
        
        self.current = self.current.prev.track
        print(f"Playing: {self.current}")

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        status = "On" if self.shuffle else "Off"
        print(f"Shuffle is now {status}.")

    def toggle_repeat(self):
        self.repeat = not self.repeat
        print(f"Repeat mode is now {'enabled' if self.repeat else 'disabled'}.")

    def add_tracks(self, new_tracks):
        for track in new_tracks:
            self.list.append(track)
        if not self.current:
            self.current = self.list[0]
        self.update_duration()

        print(f"Added {len(new_tracks)} tracks to the queue.")

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
    
    def display_queue(self):
        if not self.list:
            print("The queue is empty.")
            return

        total_pages = (len(self.list) + self.pagination - 1) // self.pagination
        current_page = self.current_index // self.pagination + 1 if self.current_index is not None else 1

        print(f"Total Duration: {self.total_duration // 3600} hr {self.total_duration % 3600 // 60} min")
        print(f"Shuffle: {'On' if self.shuffle else 'Off'} | Repeat: {'On' if self.repeat else 'Off'}")
        print(f"Page {current_page} of {total_pages}")
        print("Tracks:")

        start = (current_page - 1) * self.pagination
        end = min(start + self.pagination, len(self.list))
        for i in range(start, end):
            prefix = "(Currently Playing)" if i == self.current_index else f"({i + 1})"
            track = self.list[i]
            print(f"{prefix} {track.title} - {track.artist} ({track.duration})")


    def exit(self):
        self.save_queue()
        print("Queues saved.")


    def queue_menu(self):
        while True:
            print("\nQueue Menu:")
            print("[1] Play")
            print("[2] Skip")
            print("[3] Previous")
            print("[4] Toggle Repeat")
            print("[5] Toggle Shuffle")
            print("[6] Display Queue")
            print("[7] Save Queue")
            print("[8] Load Queue")
            print("[9] Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.play()
            elif choice == "2":
                self.skip()
            elif choice == "3":
                self.previous()
            elif choice == "4":
                self.toggle_repeat()
            elif choice == "5":
                self.toggle_shuffle()
            elif choice == "6":
                self.display_queue()
            elif choice == "7":
                self.save_queue()
            elif choice == "8":
                self.load_queue()
            elif choice == "9":
                print("Exiting queue interface.")
                break
            else:
                print("Invalid choice. Please try again.")