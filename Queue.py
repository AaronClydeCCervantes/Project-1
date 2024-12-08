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
