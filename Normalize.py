# Import libraries
from pydub import AudioSegment, effects
import os.path

# Determine main program directory
maindirectory = os.path.dirname(os.path.abspath(__file__)) # The absolute path to this file

directory= os.path.join(maindirectory,"DownloadedSongs")
try:
    music_dict = [x for x in os.listdir(directory) if ".ogg" or ".OGG" or ".Ogg" in x]
    music_count = len(music_dict)
except FileNotFoundError:
    print("[WARN] Directory not found. Exiting ...")
    quit()

counter = 1

for file in music_dict:
    print(f"[INFO] ({counter}/{music_count}) Normalizing {file}.")
    rawsound = AudioSegment.from_file(maindirectory + "/DownloadedSongs/" + str(file), "ogg")  
    normalizedsound = effects.normalize(rawsound)  
    normalizedsound.export(maindirectory + "/DownloadedSongs/" + str(file), format="ogg")
    counter += 1

print("Success!")