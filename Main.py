import json
# from Music_Library import MusicLibrary
# from Playlist import Playlist
# from Track import Track
# from Data_Storage import DataStorage
# import random

# MENUS dictionary
MENUS = {
    "main": {
        1: "Play Music",
        2: "Music Library",
        3: "Playlists",
        4: "Exit"
    },
    "Music_Library": {
        1: "Add Track",
        2: "View Tracks",
        3: "Search Tracks",
        4: "Go Back to Main Menu"
    },
    "Playlist": {
        1: "Create Playlist",
        2: "View Playlists",
        3: "Add Track to Playlist",
        4: "Go Back to Main Menu"
    }
}

def show_menu(menu_name):
    """Displays a menu and gets user choice, ensuring input is valid."""
    print(f"\n{menu_name} Menu:")
    # Display all menu options with proper numbering
    for key, value in MENUS[menu_name].items():
        print(f"{key}. {value}")
    
    # Ensure the input is a valid menu option
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice in MENUS[menu_name]:
                return str(choice)  # Return the choice as a string, since inputs are compared as strings
            else:
                print("Invalid choice. Please enter a number corresponding to the menu options.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Ensure the main menu, play music, library, and playlist menus work with this validation.


def main():
    """Main function to handle the program's execution flow."""

    # Main menu loop
    while True:
        choice = show_menu("main")
        if choice == "1":
            pass
        elif choice == "2":
            show_menu("Music Library")
            pass
        elif choice == "3":
            show_menu("Playlist")
            pass
        elif choice == "4":
            # Save data and exit
            print("Program Terminated")
            break
        else:
            print("Invalid choice. Please try again.")

# -----------------------------
# RUN THE PROGRAM
# -----------------------------
main()