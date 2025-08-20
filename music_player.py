import pygame
import os
import keyboard  # Import keyboard module for key press detection

# Initialize pygame mixer
pygame.mixer.init()

# List of songs
songs = [
    r"C:\Users\Chandrashekhar B N\Downloads\WhatsApp Audio 2025-01-27 at 4.57.31 PM.mpeg",
    r"C:\Users\Chandrashekhar B N\Downloads\WhatsApp Audio 2025-01-27 at 4.38.59 PM.mpeg",
    r"C:\Users\Chandrashekhar B N\Downloads\bad-boys_4Xmz38h3.mp3",
    r"C:\Users\Chandrashekhar B N\Downloads\Maadeva-Sanjith-Hegde-Hanumankind-Charan-Raj.mp3",
    r"C:\Users\Chandrashekhar B N\Downloads\WhatsApp Audio 2025-01-27 at 4.57.06 PM.mpeg",
    r"C:\Users\Chandrashekhar B N\Downloads\Aarambha Aarambha.mp3"
]

# Track the current song index
song_index = 0

def play_next_song():
    """Plays the next song from the list and listens for 'q' to stop."""
    global song_index

    if song_index >= len(songs):
        song_index = 0  # Reset to first song if all are played

    song_path = songs[song_index]

    if os.path.exists(song_path):
        print(f"Playing: {song_path}")
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
    else:
        print(f"Error: File {song_path} not found!")
        return  # Stop execution if the file is missing

    song_index += 1  # Move to the next song

    # Listen for 'q' key press to stop the song
    while pygame.mixer.music.get_busy():  # While music is playing
        if keyboard.is_pressed('q'):
            stop_song()
            print("Music stopped by user (pressed 'q').")
            break  # Exit the loop when 'q' is pressed

def stop_song():
    """Stops the currently playing song."""
    pygame.mixer.music.stop()
