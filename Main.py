# MIT License

# Copyright (c) 2021 Matt Curtis

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Import Modules
import random # Random number generation
import pyttsx3 # Fallback text to speech
from pydub import AudioSegment, effects # Audio normalization
import youtube_dl # Video downloading
import time # Sleep and wait commands
from datetime import datetime # Tell the date on air, as well as determine which playlist based on weekday and time
import os # Run external commands in Linux [1/2]
import os.path # Run external commands in Linux [2/2]
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hide PyGame welcome message
import pygame # Sound mixing [1/2]
import pygame.mixer, pygame.time # Sound mixing [2/2]
from selenium import webdriver # Scrape websites for information [1/3]
from selenium.webdriver import FirefoxOptions # Scrape websites for information [2/3]
from selenium.webdriver.common.keys import Keys # Inject keystrokes into webdriver [3/3]
import requests, json # Gather weather info from Openweathermap
import sys # Used to restart the script at midnight, as well as script args
import platform # Identify which OS the script is running on
import json # Parse JSON files for API and playlist info
# from textgenrnn import textgenrnn # AI-based text generation
from google.cloud import texttospeech # [PAID] Google Cloud Text to Speech

# Custom Modules
from PlaylistSearch import Playlist # Set URL, weekday text, etc. Plus, download playlists
from WeatherResponses import WeatherSpeech # Return specific sentence based on weather conditions

# Setup AI text generation
# textgen = textgenrnn()
# print("[INFO] Test phrase: " + str(textgen.generate()), end="\n\n") # Debug, print random AI-generated sentence to stdout

# Init TTS engine
engine = pyttsx3.init()
# engine.setProperty('rate', 185) # Set speech rate
engine.setProperty('volume',1.0) # Set speech volume

# Init random number generation
random.seed(a=None, version=2) # Set random seed based on current time

# Init audio engine with 10 channels
mixer = pygame.mixer
mixer.init()
mixer.set_num_channels(10)

# Determine main program directory
maindirectory = os.path.dirname(os.path.abspath(__file__)) # The absolute path to this file

# Retrieve options from JSON file
with open(str(maindirectory) + '/Options.json', 'r') as json_file:
    options_dict = json.load(json_file)

# Options
playintro = options_dict["playintro"] # Play the radio show intro on launch
wavenet = options_dict["wavenet"] # Bool for whether or not to use Google TTS API
waitforuser = options_dict["waitforuser"] # Bool for whether or not to wait for user input before starting radio
predownload = options_dict["predownload"] # Bool for whether or not to download the entire music playlist ahead of time
defaultpsachance = options_dict["defaultpsachance"] # Likelihood of playing a PSA [1/[x] chance]
defaultweatherchance = options_dict["defaultweatherchance"] # Likelihood of mentioning the weather [1/[x] chance]
defaultwelcomechance = options_dict["defaultwelcomechance"] # Likelihood of mentioning the welcome message again [1/[x] chance]
defaultweekdaychance = options_dict["defaultweekdaychance"] # Likelihood of mentioning the weekday again [1/[x] chance]
defaulttimechance = options_dict["defaulttimechance"] # Likelihood of mentioning the time [1/[x] chance]
city_name = options_dict["city_name"] # Name of city for weather info
overrideplaylist = options_dict["overrideplaylist"] # Override YouTube playlist URL for music
writeoutput = options_dict["writeoutput"] # Whether or not to print the announcer subtitles to Output.txt
writesonginfo = options_dict["writesonginfo"] # Whether or not to print the song title to SongInfo.txt
psaplaylisturl = options_dict["psaplaylisturl"] # YouTube playlist URL for PSAs
scrollinglimit = options_dict["scrollinglimit"] # Number of times to scroll down on a YouTube Playlist (affects load times, but adds more videos to playlist)

# Declare System Variables
longspeechstring = "" # Used to append multiple strings before synthesizing audio
playpsa = False # Bool value for whether or not a PSA will play immediately following a song
listPlayedSongs = [] # List stores all song numbers that have already been played
potentialsong = 1 # The index of the song to be played
psachance = defaultpsachance # Likelihood of playing a PSA [1/[x] chance]
weatherchance = defaultweatherchance # Likelihood of mentioning the weather [1/[x] chance]
welcomechance = defaultwelcomechance # Likelihood of mentioning the welcome message again [1/[x] chance]
weekdaychance = defaultweekdaychance # Likelihood of mentioning the weekday again [1/[x] chance]
timechance = defaulttimechance # Likelihood of mentioning the time [1/[x] chance]
VERSION_INFO = "21.3.7" # Script version number [YEAR.MONTH.BUILDNUM]
savedtime = "" # The text version of the time. Used to compare to actual time and determine when to start the next playlist

# Override radio intro if specified by script args
if len(sys.argv) > 1:
    if "skipintro" in sys.argv:
        playintro = False
        print("[INFO] Script arguments specified playintro to False! Skipping radio intro sequence.", end="\n\n")

# Retrieve API keys from JSON file
with open(str(maindirectory) + '/APIKeys.json', 'r') as json_file:
    APIkeys_dict = json.load(json_file)

# API Keys
weatherkey = str(APIkeys_dict["Openweathermap"]) # API key for Openweathermap
pafyAPIkey = str(APIkeys_dict["YouTube"]) # API key for YouTube video requests

# Determine the amount of random radio sounds available
DIR= os.path.join(maindirectory,"Assets/SoundEffects")
radiosoundcount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

# Determine the amount of waiting songs available
DIR= os.path.join(maindirectory,"Assets/Music")
radiomusiccount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

# Automatically set Google Environment var with API Key based on platform (Win and Mac untested)
# [ THIS IS AUTOMATICALLY OVERRIDDEN BY STARTRADIO SCRIPT ]
# if str(platform.system()) == "Linux":
#     os.system('export GOOGLE_APPLICATION_CREDENTIALS="' + str(maindirectory).replace(" ","\ ") + '/GoogleAPIKey.json"')
# elif str(platform.system()) == "Darwin":
#     os.system('export GOOGLE_APPLICATION_CREDENTIALS="' + str(maindirectory) + '/GoogleAPIKey.json"')
# # elif str(platform.system()) == "Windows":
#     os.system('export GOOGLE_APPLICATION_CREDENTIALS="' + str(maindirectory) + '\GoogleAPIKey.json"')

# Google Cloud TTS Function to Generate Wavenet Samples
def text_to_wav(text, earlyfade = False):
    # If the current time is in the early morning, save money by switching to Standard voice
    timeobject = datetime.now()
    currenttime = int(timeobject.strftime("%H"))
    if currenttime >= 0 and currenttime < 8:
        voice_name = "en-US-Standard-I"
    else:
        voice_name = "en-US-Wavenet-I"
    
    # Uncomment the following line to force Standard voice
    # voice_name = "en-US-Standard-I"

    language_code = "-".join(voice_name.split("-")[:2])
    text_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=1.00,
        pitch=-5
    )

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    filename = f"{language_code}.wav"
    with open(str(maindirectory) + "/" + filename, "wb") as out:
        out.write(response.audio_content)

    voice = mixer.Sound(str(maindirectory) + "/en-US.wav")
    voice.set_volume(1)
    mixer.Channel(0).play(voice, fade_ms=0)
    if earlyfade: # If specified, continue running code 5 seconds before sound ends
        waittime = (voice.get_length()*1000) - 5000
        if waittime < 0:
            waittime = voice.get_length()*1000
        # pygame.time.wait(waittime)
        time.sleep(waittime/1000)
    else:
        time.sleep(voice.get_length())

# Custom function to just speak text with system TTS
def speaktext(message, earlyfade = False):
    print("[SPEECH] " + "\"" + str(message) + "\"", end="\n\n") # Print the message contents to stdout
    # If enabled, write message contents to text file for use in OBS Studio
    if writeoutput == True:
        with open(str(maindirectory) + "/Output.txt","w") as fileoutput:
            fileoutput.write("\n" + str(message))
            fileoutput.close()
    if wavenet == True:
        if earlyfade:
            text_to_wav(str(message), earlyfade=True)
        else:
            text_to_wav(str(message), earlyfade=False)
    else:
        # If platform is Mac OS or Windows, use system TTS
        if str(platform.system()) == "Darwin" or str(platform.system()) == "Windows":
            engine.say(str(message)) # System TTS [1/2]
            engine.runAndWait() # System TTS [2/2]
        else: # On Linux, use MBROLA or espeak
            os.system("espeak -p 50 -s 165 -v mb/mb-us2 \"" + str(message).replace("'","").replace("\"","") + "\"") # MBROLA TTS
            # engine.say(str(message)) # System TTS [1/2]
            # engine.runAndWait() # System TTS [2/2]

# Tell user that the program is starting
speaktext("The radio will be back online in a moment!")

# Start a random radio "waiting" song
waitingsound = mixer.Sound(str(maindirectory) + "/Assets/Music/" + str(random.randint(1,radiomusiccount)) + ".WAV")
waitingsound.set_volume(0.4)
mixer.Channel(1).play(waitingsound, fade_ms=1000, loops=999)

# State any errors/warnings to user
if weatherkey == "":
    print("[INFO] " + "You have not provided an Openweathermap API key. The API key is required to give weather info.", end="\n\n")

# Custom function to remove unneccessary chars from YouTube video ID after "&"
def vidstrip(playlist):
    for i in range(len(playlist)):
        end=playlist[i].find("&")
        playlist[i]=playlist[i][:end]
    return playlist

# Clear url VAR
url = ""

# Display time to stdout to let user verify if correct playlist is chosen.
timeobject = datetime.now()
currenttime = timeobject.strftime("%I:%M")
print("[INFO] " + "The time is currently " + str(currenttime) + ".", end="\n\n")

# Set the following VARs according to the current time, for use in the IF statements below
timeobject = datetime.now()
currenttime = int(timeobject.strftime("%H"))

# Set the appropriate playlist according to the weekday using custom PlaylistSearch function w/ classes
playlistselection = Playlist(datetime.today().weekday(), currenttime)
url = playlistselection.get_URL()
savedweekday = playlistselection.get_savedweekday()
savedtime = playlistselection.get_savedtime()
weekdaytext = playlistselection.get_weekdaytext()

# If the playlist URL is still blank, warn the user and use a fallback playlist
if url == "":
    url = "https://www.youtube.com/playlist?list=PLHL1i3oc4p0o76QOZ_BLZwjDb1x21azmC"
    print("[INFO] " + "You didn't specify a music playlist for today's date! Using fallback playlist.", end="\n\n")

# If specified, override the weekday playlist with something else
if overrideplaylist:
    url = overrideplaylist
    print("[INFO] " + "Override enabled for playlist. Using " + str(url) + ".", end="\n\n")

# Print steps to stdout
print("[INFO] " + "Scraping music playlist ...", end="\n\n")

# Set Firefox to run in headless mode
opts = FirefoxOptions()
opts.add_argument("--headless")
driver = webdriver.Firefox(options=opts)

# Open playlist URL in headless Firefox
driver.get(url)

# Declare lists for playlist video URLs and titles
playlist=[]
playlistnames=[]
countervar = 1 # Used to display how many videos have been gathered

# Continue to scroll down the playlist until most of playlist is in view
scrollcounter = 0
while scrollcounter < scrollinglimit:
    scrolldriver = driver.find_element_by_tag_name("html")
    scrolldriver.send_keys(Keys.END)
    time.sleep(2)
    scrollcounter += 1
    print(f"[INFO] (Index {scrollcounter}) Scrolling to next page in playlist.", end="\n\n")

videos=driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')

# Scrape each video into two lists, video URLs and video titles respectively
for video in videos:
    link=video.find_element_by_xpath('.//*[@id="video-title"]').get_attribute("href")
    longname=video.find_element_by_xpath('.//*[@id="video-title"]').get_attribute("title")
    end=longname.find("(")
    if end == -1 and end != 0:
        longname_concat = longname
    else:
        longname_concat = longname[:end]
    
    end=longname_concat.find("[")
    if end == -1 and end != 0:
        name = longname_concat.title()
    else:
        name = longname_concat[:end].title()
    if name != "": # If title exists, add name and link to the lists
        print(f"[INFO] (Video Index {str(countervar)}) Retrieved info for \"{name}\"", end="\n\n")
        playlist.append(link)
        playlistnames.append(name)
        countervar += 1

musicplaylist=vidstrip(playlist) # Strip unneccessary chars from list
driver.close() # Close the web rendering engine

# Print message to stdout
print("[INFO] " + "Finished downloading info from music playlist.", end="\n\n")

# If predownload is enabled, download entire music library ahead of time
if predownload:
    print("[INFO] " + "Saving music playlist to disk ...", end="\n\n")
    speaktext("Please enjoy this song while I finish preparing a playlist for you. This will take a while.")
    # Download first 100 videos from playlist.
    ydl_opts = {"outtmpl": str(maindirectory) + "/DownloadedSongs/%(id)s.%(ext)s", "ignoreerrors": True, "format": "bestaudio[ext=m4a]", "geobypass": True, "noplaylist": True, "source_address": "0.0.0.0", "download_archive": str(maindirectory) + "/SongArchive.txt", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "vorbis"}]}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(playlist[:100])

# Next, scrape the PSA playlist (if playlist URL is specified)
if psaplaylisturl != "":
    # Set URL for PSAs instead of music
    url = psaplaylisturl

    # Print steps to stdout
    print("[INFO] " + "Scraping PSA playlist ...", end="\n\n")

    # Run Firefox in automated headless mode
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)
    driver.get(url) # Open URL
    playlist=[] # Clear "playlist" list
    playlistnamesPSA=[]
    countervar = 1 # Used to display how many videos have been gathered

    # Continue to scroll down the playlist until most of playlist is in view
    scrollcounter = 0
    while scrollcounter < scrollinglimit:
        scrolldriver = driver.find_element_by_tag_name("html")
        scrolldriver.send_keys(Keys.END)
        time.sleep(2)
        scrollcounter += 1
        print(f"[INFO] (Index {scrollcounter}) Scrolling to next page in playlist.", end="\n\n")

    videos=driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')
    for video in videos:
        link2=video.find_element_by_xpath('.//*[@id="video-title"]').get_attribute("href")
        longname2=video.find_element_by_xpath('.//*[@id="video-title"]').get_attribute("title")
        end=longname2.find("(")
        if end == -1 and end != 0:
            longname_concat = longname2
        else:
            longname_concat = longname2[:end]
        
        end=longname_concat.find("[")
        if end == -1 and end != 0:
            name = longname_concat.title()
        else:
            name = longname_concat[:end].title()
        if name != "": # If title exists, add name and link to the lists
            playlist.append(link2) # Append each URL to the list
            playlistnamesPSA.append(longname2)
            print(f"[INFO] (Video Index {str(countervar)}) Retrieved info for \"{longname2}\"", end="\n\n")
            countervar += 1

    psaplaylist=vidstrip(playlist)
    driver.close() # Close the web rendering engine
else:
    # Print missing playlist info message to stdout
    print("[INFO] " + "PSA playlist URL has not been set. The station will not play PSAs.", end="\n\n")

# Print completion message to stdout
print("[INFO] " + "Finished downloading info from PSA playlist. Starting radio ...", end="\n\n")

# Read and store each external speech script into memory
# (Each line in the textfile represents a different index in the list)
# This is used for text variation to make the announcer seem more lifelike.

# Intro Text Short (Single sentence to welcome the listener)
fileIntroTextShort = open(str(maindirectory) + "/SpeechScripts/IntroTextShort.txt", "r")
speechIntroTextShort = fileIntroTextShort.readlines()
fileIntroTextShort.close()

# First Run Prompts (Describes the radio station in-detail)
fileFirstrunPrompts = open(str(maindirectory) + "/SpeechScripts/FirstrunPrompts.txt", "r")
speechFirstrunPrompts = fileFirstrunPrompts.readlines()
fileFirstrunPrompts.close()

# Song Transitions (Variations on describing which song comes next)
fileSongTransitions = open(str(maindirectory) + "/SpeechScripts/SongTransitions.txt", "r")
speechSongTransitions = fileSongTransitions.readlines()
fileSongTransitions.close()

# Song END Transitions (Variations on what song you just heard)
fileSongEndTransitions = open(str(maindirectory) + "/SpeechScripts/SongEndTransitions.txt", "r")
speechSongEndTransitions = fileSongEndTransitions.readlines()
fileSongEndTransitions.close()

# Prepare the intro lines with synthesized voice
longspeechstring = "" # Clear the longspeechstring var

# If the playlist isn't overridden, add the weekday text to longspeechstring var
if not overrideplaylist:
    longspeechstring += str(weekdaytext)

# Add a random variation of the "Intro Text Short" speech to longspeechstring var & include the version number
longspeechstring += " " + str(speechIntroTextShort[random.randint(0,len(speechIntroTextShort)-1)])
longspeechstring += " Version " + str(VERSION_INFO) + "."

# Add a random variation of the "First Run Prompts" speech to longspeechstring var
longspeechstring += " " + str(speechFirstrunPrompts[random.randint(0,len(speechFirstrunPrompts)-1)])

# Stop the waiting sound, fading out for 1 second
waitingsound.fadeout(1000)

# Wait for the user to press ENTER if they specified waiting in Options.json
if waitforuser:
    print("[INFO] The radio is ready! Press ENTER to start.")
    testinput = input("")

# Loop through songs, announcements, and other commentary forever
while True:
    try: # Uses "try except" loop, ensuring that if an error occurs, the script will restart automatically
        # Set the random seed again based on current time
        random.seed(a=None, version=2)
        
        # Play radio intro if enabled
        if playintro == True:
            # Play random radio sound before speaking (if file exists)
            if radiosoundcount >= 1:
                sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects/" + str(random.randint(1,radiosoundcount)) + ".WAV")
                sound.set_volume(0.3)
                mixer.Channel(2).play(sound, fade_ms=0)
                waittime = (sound.get_length()*1000)/2
                if waittime < 0:
                    waittime = sound.get_length()*1000
                # pygame.time.wait(waittime)
                time.sleep(waittime/1000)
            
            # Play the background waiting sound while the announcer speaks
            newwaitingsound = mixer.Sound(str(maindirectory) + "/Assets/Music/" + str(random.randint(1,radiomusiccount)) + ".WAV")
            newwaitingsound.set_volume(0.2)
            mixer.Channel(3).play(newwaitingsound, fade_ms=1000)

            # Play the synthesized voice
            speaktext(longspeechstring)

            # Stop the waiting sound, fading out for 1 second
            newwaitingsound.fadeout(1000)

            # Play random radio sound after speaking (if file exists)
            if radiosoundcount >= 1:
                sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects/" + str(random.randint(1,radiosoundcount)) + ".WAV")
                sound.set_volume(0.3)
                mixer.Channel(4).play(sound, fade_ms=0)
                waittime = (sound.get_length()*1000)/2
                if waittime < 0:
                    waittime = sound.get_length()*1000
                # pygame.time.wait(waittime)
                time.sleep(waittime/1000)

            # Choose the first song to play
            if len(listPlayedSongs) >= len(musicplaylist) - 1: # If the music list has been exhausted
                listPlayedSongs.clear() # Clear the list and start again
            potentialsong = random.randint(1,len(musicplaylist)-1) # Choose a random song index from the playlist
            while potentialsong in listPlayedSongs: # If the song has been chosen already,
                potentialsong = random.randint(1,len(musicplaylist)-1) # Randomly select a new song from the playlist
            listPlayedSongs.append(potentialsong) # Add the song index to the list of played songs
            songselectionint = potentialsong # Set the next song to the one that was randomly chosen
            print("[INFO] " + "List of completed song indexes:\n\t" + str(listPlayedSongs), end="\n\n") # Show list of played song numbers
            print("[INFO] " + "Likelihood VARs:\n\tPSA: [1/" + str(psachance) + "]\tWeather: [1/" + str(weatherchance) + "]\tWelcomeMessage: [1/" + str(welcomechance) + "]\tWeekdayMessage: [1/" + str(weekdaychance) + "]\tTime: [1/" + str(timechance) + "]", end="\n\n") # Show chance VARs

            longspeechstring = "" # Clear the longspeechstring var
            longspeechstring += " " + str(speechSongTransitions[random.randint(0,len(speechSongTransitions)-1)]) + str(playlistnames[songselectionint]) + "."
            # longspeechstring += " " + str(speechSongTransitions[random.randint(0,len(speechSongTransitions)-1)]) + str(playlistnames[songselectionint]) + "."
            
            # Chance to speak "Stay safe out there!"
            if random.randint(0,4) == 1:
                longspeechstring += " Stay safe out there!"
            
            # Use system TTS engine to speak the next song info
            speaktext(longspeechstring, earlyfade=True)

            # Play random radio sound after speaking (if file exists)
            if radiosoundcount >= 1:
                sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects/" + str(random.randint(1,radiosoundcount)) + ".WAV")
                sound.set_volume(0.3)
                mixer.Channel(4).play(sound, fade_ms=0)
                waittime = (sound.get_length()*1000)/2
                if waittime < 0:
                    waittime = sound.get_length()*1000
                # pygame.time.wait(waittime)
                time.sleep(waittime/1000)

            # Prevent the intro from playing again on next loop
            playintro = False

        # [ [ [ CURRENTLY NOT WORKING ] ] ]
        # If writesonginfo is enabled, write the song title to SongInfo.txt
        # if writesonginfo == True:
        #     with open(str(maindirectory) + "/SongInfo.txt","w") as fileoutput2:
        #         fileoutput2.write(str(playlistnames[songselectionint])
        #         fileoutput2.close()

        # Clear the longspeechstring var
        longspeechstring = ""

        # If the file has not been downloaded, do the following
        if not os.path.exists(str(str(maindirectory) + "/DownloadedSongs/" + str(musicplaylist[songselectionint]) + ".ogg").replace("https://www.youtube.com/watch?v=","")):
            # Download the next song as a OGG file with YouTube-DL
            ydl_opts = {"outtmpl": str(maindirectory) + "/DownloadedSongs/%(id)s.%(ext)s", "ignoreerrors": True, "format": "bestaudio[ext=m4a]", "geobypass": True, "source_address": "0.0.0.0", "noplaylist": True, "download_archive": str(maindirectory) + "/SongArchive.txt", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "vorbis"}]}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                # ydl.download(str(musicplaylist[songselectionint]))
                info = ydl.extract_info(str(musicplaylist[songselectionint]), download=True)

        # Normalize the audio
        beforesound = AudioSegment.from_file(str(str(maindirectory) + "/DownloadedSongs/" + str(musicplaylist[songselectionint]) + ".ogg").replace("https://www.youtube.com/watch?v=",""), "ogg")  
        aftersound = effects.normalize(beforesound)  
        aftersound.export(str(str(maindirectory) + "/DownloadedSongs/" + str(musicplaylist[songselectionint]) + ".ogg").replace("https://www.youtube.com/watch?v=",""), format="ogg")

        # Play the downloaded song with pygame mixer
        music = mixer.Sound(str(str(maindirectory) + "/DownloadedSongs/" + str(musicplaylist[songselectionint]) + ".ogg").replace("https://www.youtube.com/watch?v=",""))
        music.set_volume(0.7)
        mixer.Channel(5).play(music, fade_ms=5000)
        waittime = (music.get_length()*1000) - 5000
        if waittime < 0:
            waittime = music.get_length()*1000
        if waittime > 600000: # If song is greater than 10 minutes
            waittime = 600000 # Set length to maximum of 10 minutes
            longspeechstring += "That's enough of that song. "
        # pygame.time.wait(waittime)
        # Show operator that song is playing in stdout
        print("[INFO] " + "Currently playing " + str(playlistnames[songselectionint]) + ".", end="\n\n")
        print("[DEBUG - SONG PATH] " + str(str(maindirectory) + "/DownloadedSongs/" + str(musicplaylist[songselectionint]) + ".ogg").replace("https://www.youtube.com/watch?v=",""), end="\n\n")
        time.sleep(waittime/1000)
        music.fadeout(5000)

        # Song that just played
        longspeechstring += str(speechSongEndTransitions[random.randint(0,len(speechSongEndTransitions)-1)]) + str(playlistnames[songselectionint]) + "."

        # Listening to PhysCorp's Automated Station & Version Info
        longspeechstring += " " + str(speechIntroTextShort[random.randint(0,len(speechIntroTextShort)-1)])
        longspeechstring += " Version " + str(VERSION_INFO) + "."

        # Chance to mention the time
        if random.randint(0, timechance) == 1:
            timeobject = datetime.now()
            currenttime = timeobject.strftime("%I:%M")
            longspeechstring += " The time is currently " + str(currenttime) + "."
            timechance = defaulttimechance

        # Increase the chance to speak the time
        if timechance > 2:
            timechance -= 1

        # Chance to mention one of the "First Run Prompts" again
        if random.randint(0, welcomechance) == 1:
            # Add a random variation of the "First Run Prompts" speech to longspeechstring var
            longspeechstring += " If you just tuned in, " + str(speechFirstrunPrompts[random.randint(0,len(speechFirstrunPrompts)-1)])
            # Reset welcomechance var
            welcomechance = defaultwelcomechance

        # Increase the chance to speak the welcome message
        if welcomechance > 2:
            welcomechance -= 1

        # Chance to talk about the weather [copied from online tutorial]
        # Only talks about weather if the welcome message didn't just play
        if random.randint(0,weatherchance) == 1 and weatherkey != "" and welcomechance != defaultwelcomechance-1:
            # Reset weatherchance var
            weatherchance = defaultweatherchance

            # Talk about weather using Openweathermap API

            # My API key
            api_key = weatherkey

            # base_url variable to store the Openweathermap URL 
            base_url = "http://api.openweathermap.org/data/2.5/weather?"

            # Set city name [REFERENCED IN MAIN.PY OPTIONS]
            # If blank, set city to Auburn Hills and print info to stdout
            if city_name == "":
                city_name = "Auburn Hills"
                print("[INFO] " + "A city name has not been set. Using Auburn Hills.", end="\n\n")

            # complete_url variable to store 
            # complete url address 
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name 

            # get method of requests module 
            # return response object 
            response = requests.get(complete_url) 

            # json method of response object 
            # convert json format data into 
            # python format data 
            x = response.json() 

            # Now x contains list of nested dictionaries 
            # Check the value of "cod" key is equal to 
            # "404", means city is found otherwise, 
            # city is not found 
            if x["cod"] != "404": 

                # store the value of "main" 
                # key in variable y 
                y = x["main"] 

                # store the value corresponding 
                # to the "temp" key of y 
                current_temperature = (y["temp"])*1.8 - 459.67

                # store the value corresponding 
                # to the "humidity" key of y 
                current_humidity = y["humidity"] 

                # store the value of "weather" 
                # key in variable z 
                z = x["weather"] 

                # store the value corresponding 
                # to the "description" key at 
                # the 0th index of z 
                weather_description = z[0]["description"] 

                # Include weather info in longspeechstring var
                longspeechstring += " Let's check up on the weather outside! " 
                weatherobject = WeatherSpeech(str(weather_description))
                longspeechstring += weatherobject.returnspeech() + ". "
                longspeechstring += "The temperature is currently " + str(round(current_temperature)) + " degrees."


        # Increase the chance to speak the weather info
        if weatherchance > 2:
            weatherchance -= 1
        
        # Randomly choose a new song from the playlist
        if len(listPlayedSongs) >= len(musicplaylist) - 1: # If the music list has been exhausted
            listPlayedSongs.clear() # Clear the list and start again
        while potentialsong in listPlayedSongs: # If the song has been chosen already,
            potentialsong = random.randint(1,len(musicplaylist)-1) # Randomly select a new song from the playlist
        listPlayedSongs.append(potentialsong) # Add the song index to the list of played songs
        songselectionint = potentialsong # Set the next song to the one that was randomly chosen
        print("[INFO] " + "List of completed song indexes:\n\t" + str(listPlayedSongs), end="\n\n") # Show list of played song numbers
        print("[INFO] " + "Likelihood VARs:\n\tPSA: [1/" + str(psachance) + "]\tWeather: [1/" + str(weatherchance) + "]\tWelcomeMessage: [1/" + str(welcomechance) + "]\tWeekdayMessage: [1/" + str(weekdaychance) + "]\tTime: [1/" + str(timechance) + "]", end="\n\n") # Show chance VARs
        
        # If the playlist isn't overridden, chance to add the weekday text to longspeechstring var
        if not overrideplaylist:
            if random.randint(0,weekdaychance) == 1:
                longspeechstring += " " + str(weekdaytext)
                # Reset weekdaychance var
                weekdaychance = defaultweekdaychance
            # Increase the chance to speak the current weekday
            if weekdaychance > 2:
                weekdaychance -= 1

        # Add the next song info to the longspeechstring var
        # longspeechstring += " " + str(speechSongTransitions[random.randint(0,len(speechSongTransitions)-1)]) + str(playlistnames[songselectionint]) + "."
        longspeechstring += " " + str(speechSongTransitions[random.randint(0,len(speechSongTransitions)-1)]) + str(playlistnames[songselectionint]) + "."

        # Chance to play a PSA
        if random.randint(0,psachance) == 1 and psaplaylisturl != "":
            playpsa = True
            longspeechstring += " But first, here's a brief message. Don't touch that dial."
            # Reset psachance var
            psachance = defaultpsachance

        # Chance to include "Stay safe out there!" in speech
        if random.randint(0,4) == 1:
            longspeechstring += " Stay safe out there!"

        # Play random radio sound before speaking if file exists
        if radiosoundcount >= 1:
            sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects/" + str(random.randint(1,radiosoundcount)) + ".WAV")
            sound.set_volume(0.3)
            mixer.Channel(6).play(sound, fade_ms=0)
            waittime = (sound.get_length()*1000)/2
            if waittime < 0:
                waittime = sound.get_length()*1000
            # pygame.time.wait(waittime)
            time.sleep(waittime/1000)
        
        # Play the background waiting sound while the announcer speaks
            newwaitingsoundtwo = mixer.Sound(str(maindirectory) + "/Assets/Music/" + str(random.randint(1,radiomusiccount)) + ".WAV")
            newwaitingsoundtwo.set_volume(0.2)
            mixer.Channel(7).play(newwaitingsoundtwo, fade_ms=1000)

        # If the time is midnight (if stored weekday info doesn't match current weekday info), restart the script to gather new playlist info
        if savedweekday != datetime.today().weekday():
            speaktext("It's midnight. I'm switching to a new playlist. Please wait.")
            newwaitingsoundtwo.fadeout(1000)
            os.execv(sys.executable, ['python3'] + sys.argv) # Restart the script by issuing a terminal command
        
        # Compared the savedtime VAR to the current time text. If mismatch, restart the station with a new playlist
        timeobject = datetime.now()
        currenttime = int(timeobject.strftime("%H"))

        if currenttime >= 0 and currenttime < 8: # Early Morning
            savedtimecomparison = "Early Morning"

        elif currenttime >= 8 and currenttime < 12: # Morning
            savedtimecomparison = "Morning"

        elif currenttime >= 12 and currenttime < 16: # Afternoon
            savedtimecomparison = "Afternoon"

        elif currenttime >= 16 and currenttime < 20: # Evening
            savedtimecomparison = "Evening"
        
        elif currenttime >= 20 and currenttime < 24: # Late Night
            savedtimecomparison = "Late Night"
        
        # If mismatch, restart the station
        if savedtimecomparison != savedtime:
            speaktext("I'm switching to a new playlist. Please wait.")
            waitingsound.stop()
            os.execv(sys.executable, ['python3'] + sys.argv) # Restart the script by issuing a terminal command

        # Play the synthesized speech
        speaktext(longspeechstring)

        # Stop the waiting sound, fading out for 1 second
        newwaitingsoundtwo.fadeout(1000)

        # Play the PSA if triggered
        if playpsa == True:
            playpsa = False # Prevent PSA from running twice
            
            # Play the PSA, if the video isn't available, repeat the process until one is
            while True:
                try:
                    playlistitem = str(psaplaylist[random.randint(1,len(psaplaylist)-1)])
                    if not os.path.exists(str(str(maindirectory) + "/DownloadedPSAs/" + playlistitem + ".ogg").replace("https://www.youtube.com/watch?v=","")):
                        # Download the next song as a OGG file with YouTube-DL
                        ydl_opts = {"outtmpl": str(maindirectory) + "/DownloadedPSAs/%(id)s.%(ext)s", "ignoreerrors": True, "format": "bestaudio[ext=m4a]", "geobypass": True, "source_address": "0.0.0.0", "noplaylist": True, "download_archive": str(maindirectory) + "/PSAArchive.txt", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "vorbis"}]}
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            # ydl.download(str(musicplaylist[songselectionint]))
                            info = ydl.extract_info(playlistitem, download=True)

                    # Normalize the audio
                    beforesound = AudioSegment.from_file(str(str(maindirectory) + "/DownloadedPSAs/" + playlistitem + ".ogg").replace("https://www.youtube.com/watch?v=",""), "ogg")  
                    aftersound = effects.normalize(beforesound)  
                    aftersound.export(str(str(maindirectory) + "/DownloadedPSAs/" + playlistitem + ".ogg").replace("https://www.youtube.com/watch?v=",""), format="ogg")

                    # Play the downloaded song with pygame mixer
                    psa = mixer.Sound(str(str(maindirectory) + "/DownloadedPSAs/" + playlistitem + ".ogg").replace("https://www.youtube.com/watch?v=",""))
                    psa.set_volume(0.7)
                    mixer.Channel(9).play(psa, fade_ms=1000)
                    waittime = psa.get_length()*1000
                    # pygame.time.wait(waittime)
                    # Show operator that song is playing in stdout
                    print("[INFO] " + "Currently playing PSA.", end="\n\n")
                    time.sleep(waittime/1000)

                    pass
                    break # Break out of statement
                except (RuntimeError, TypeError, NameError, OSError):
                    pass # Repeat
        
        # Increase chance to play PSA next time
        if psachance > 2:
            psachance -= 1

        # Play random radio sound after speaking if file exists
        if radiosoundcount >= 1:
            sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects/" + str(random.randint(1,radiosoundcount)) + ".WAV")
            sound.set_volume(0.3)
            mixer.Channel(8).play(sound, fade_ms=0)
            waittime = (sound.get_length()*1000)/2
            if waittime < 0:
                waittime = sound.get_length()*1000
            # pygame.time.wait(waittime)
            time.sleep(waittime/1000)
    except (RuntimeError, TypeError, NameError, OSError, KeyError, IndexError, LookupError):
        # Say that something has gone wrong
        speaktext("It looks like that song isn't available. Please wait while I find another song.")
        # longspeechstring = "" # Reset longspeechstring
        # playintro = True # Failsafe, run through intro again
        # pass
        os.execv(sys.executable, ['python3'] + sys.argv) # Restart the script by issuing a terminal command
        # os.execv(sys.executable, ['python3'] + sys.argv + ["skipintro"]) # Restart the script by issuing a terminal command, skipping the intro