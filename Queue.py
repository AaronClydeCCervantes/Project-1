import json
import random
from Track import Track

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
        if not self.list:
            return "The queue is empty. Add tracks to play."
        if self.current_index is None:
            self.current_index = 0
        self.current = self.list[self.current_index]
        return f"Playing: {self.current.title}"

    def skip(self):
        if self.current_index is None:
            return "No track is currently playing."
        if self.current_index + 1 < len(self.list):
            self.current_index += 1
        elif self.repeat:
            self.current_index = 0
        else:
            return "End of the queue."
        self.current = self.list[self.current_index]
        return f"Playing: {self.current.title}"

    def previous(self):
        if self.current_index is None:
            return "No track is currently playing."
        if self.current_index > 0:
            self.current_index -= 1
        else:
            return "No previous track. You are at the start of the queue."
        self.current = self.list[self.current_index]
        return f"Playing: {self.current.title}"

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        return f"Shuffle is now {'enabled' if self.shuffle else 'disabled'}."

    def toggle_repeat(self):
        self.repeat = not self.repeat
        return f"Repeat is now {'enabled' if self.repeat else 'disabled'}."

    def add_tracks(self, new_tracks):
        self.list.extend(new_tracks)
        if self.current is None:
            self.current_index = 0
            self.current = self.list[0]
        self.total_duration = sum(track.duration for track in self.list)
        return f"Added {len(new_tracks)} tracks to the queue."

    def display_queue(self, page_number=1):
        if not self.list:
            return "The queue is empty."

        total_pages = (len(self.list) + self.pagination - 1) // self.pagination
        page_number = max(1, min(page_number, total_pages))

        total_duration = sum(track.duration for track in self.list)
        header = f"Total Duration: {total_duration // 3600} hr {total_duration % 3600 // 60} min {total_duration % 60} sec\n"
        header += f"Shuffle: {'On' if self.shuffle else 'Off'} | Repeat: {'On' if self.repeat else 'Off'}\n"
        header += f"<Page {page_number} of {total_pages}>\n"

        start = (page_number - 1) * self.pagination
        end = min(start + self.pagination, len(self.list))
        tracks = "\n".join(
            f"({i + 1}) {track.title} – {track.artist} ({self._format_duration(track.duration)})"
            for i, track in enumerate(self.list[start:end], start=start)
        )

        return header + tracks

    def _format_duration(self, duration):
        minutes = duration // 60
        seconds = duration % 60
        return f"{minutes}:{seconds:02}"

    def save_queue(self):
        try:
            with open("queue.json", "w") as file:
                json.dump(
                    [
                        {"title": track.title, "artist": track.artist, "album": track.album, "duration": track.duration}
                        for track in self.list
                    ],
                    file,
                    indent=4,
                )
            print("Queue saved.")
        except Exception as e:
            print(f"Error saving queue: {e}")

    def load_queue(self):
        try:
            with open("queue.json", "r") as file:
                tracks = json.load(file)
            self.list = [Track(**track) for track in tracks]
            self.total_duration = sum(track.duration for track in self.list)
            self.current_index = 0 if self.list else None
            print("Queue loaded.")
        except FileNotFoundError:
            print("No saved queue found.")
        except Exception as e:
            print(f"Error loading queue: {e}")

    
