import pygame
import os

def play_mp3(file_path):
    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(file_path)

    # Play the loaded MP3 file
    pygame.mixer.music.play()

    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up
    pygame.mixer.quit()

# Example usage
mp3_file_path = r'music\钓满10条鱼了.mp3'
play_mp3(mp3_file_path)
