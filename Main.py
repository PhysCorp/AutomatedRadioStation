# Import Modules
import random # Random number generation
import pyttsx3 # Fallback text to speech
import pafy # Video downloading
import vlc # Play music and videos
import time # Sleep and wait commands
from datetime import datetime # Tell the date on air, as well as determine which playlist based on weekday and time
import re # Strip all chars except letters and numbers from a string
import pygame # Sound mixing [1/2]
import pygame.mixer, pygame.time # Sound mixing [2/2]
import os # Run external commands in Linux [1/3]
import os.path # Run external commands in Linux [2/3]
from os import path # Run external commands in Linux [3/3]
from selenium import webdriver # Scrape websites for information [1/2]
from selenium.webdriver import FirefoxOptions # Scrape websites for information [2/2]
import requests, json # Gather weather info from Openweathermap
import sys # Used to restart the script at midnight
import platform # Identify which OS the script is running on
# from textgenrnn import textgenrnn # AI-based text generation

# Setup AI text generation
# textgen = textgenrnn()
# print(str(textgen.generate())) # Debug, print random AI-generated sentence to stdout

# Init TTS engine
engine = pyttsx3.init()
# engine.setProperty('rate', 185) # Set speech rate
engine.setProperty('volume',1.0) # Set speech volume

# Init random number generation
random.seed(a=None, version=2) # Set random seed based on current time

# Init audio engine
mixer = pygame.mixer
mixer.init()

# Options
playintro = True # Play the radio show intro on launch
advancedspeech = False # Use AI-based speech generation service
defaultpsachance = 8 # Likelihood of playing a PSA [1/[x] chance]
defaultweatherchance = 10 # Likelihood of mentioning the weather [1/[x] chance]
defaultwelcomechance = 8 # Likelihood of mentioning the welcome message again [1/[x] chance]
defaultweekdaychance = 8 # Likelihood of mentioning the weekday again [1/[x] chance]
defaulttimechance = 8 # Likelihood of mentioning the time [1/[x] chance]
weatherkey = "" # API key for Openweathermap
city_name = "Auburn Hills" # Name of city for weather info
overrideplaylist = "" # Override YouTube playlist URL for music
writeoutput = False # Whether or not to print the announcer subtitles to Output.txt
writesonginfo = False # Whether or not to print the song title to SongInfo.txt
psaplaylisturl = "https://www.youtube.com/playlist?list=PLUJZiQIClkwdxdCVag0ffmjPNdnHDlb02" # YouTube playlist URL for PSAs

# Declare Variables
longspeechstring = "" # Used to append multiple strings before synthesizing audio
playpsa = False # Bool value for whether or not a PSA will play immediately following a song
listPlayedSongs = [] # List stores all song numbers that have already been played
potentialsong = 1 # The index of the song to be played
maindirectory = os.path.dirname(os.path.abspath(__file__)) # The absolute path to this file
psachance = defaultpsachance # Likelihood of playing a PSA [1/[x] chance]
weatherchance = defaultweatherchance # Likelihood of mentioning the weather [1/[x] chance]
welcomechance = defaultwelcomechance # Likelihood of mentioning the welcome message again [1/[x] chance]
weekdaychance = defaultweekdaychance # Likelihood of mentioning the weekday again [1/[x] chance]
timechance = defaulttimechance # Likelihood of mentioning the time [1/[x] chance]
versioninfo = "21.2.2" # Script version number [YEAR.MONTH.BUILDNUM]
savedtime = "" # The text version of the time. Used to compare to actual time and determine when to start the next playlist

# Determine the amount of random radio sounds available
DIR= os.path.join(maindirectory,"Assets/SoundEffects")
radiosoundcount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

# Determine the amount of waiting songs available
DIR= os.path.join(maindirectory,"Assets/Music")
radiomusiccount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

# Custom function to synthesize audio in the background [followed by speakrichtext function]
def preparevoice(message):
    if path.exists(str(maindirectory) + "/Output.wav"): # If the old file exists already
        if str(platform.system()) == "Darwin" or str(platform.system()) == "Linux":
            os.system("rm \"" + str(maindirectory) + "/Output.wav" + "\"") # Delete the old file [Linux and Mac OS]
        else:
            os.system("del \"" + str(maindirectory) + "/Output.wav" + "\"") # Delete the old file [Windows]
    # Run the neural synthesis engine asynchronously, piping all output to nohup.out
    os.system("nohup python3 \"" + str(maindirectory) + "/Real-Time-Voice-Cloning-master/demo_cli.py\" --no_sound --speechcontent \"" + str(re.sub("[\W ]+"," ",str(message).replace(".","_")).replace("_",". ")) + "\"  &")

# Speak text with neural synthesis engine first, but fallback to system TTS if the file isn't ready
def speakrichtext(message):
    # If enabled, write announcer subtitles to text file for use in OBS Studio
    if writeoutput == True:
        with open(str(maindirectory) + "/Output.txt","w") as fileoutput:
            fileoutput.write("\n" + str(message))
            fileoutput.close()
    # If the file is not ready, use fallback TTS, prepending string with "Announcer two here."
    if not path.exists(str(maindirectory) + "/Output.wav"):
        speaktext("Announcer two here. " + str(message))
    else: # If the file IS ready, play it synchronously
        sound = mixer.Sound(str(maindirectory) + "/Output.wav")
        sound.set_volume(1)
        channel = sound.play()
        while channel.get_busy():
            pygame.time.wait(100)
    longspeechstring = "" # Clear longspeechstring var

# Custom function to just speak text with system TTS
def speaktext(message):
    print(str(message)) # Print the message contents to stdout
    # If enabled, write message contents to text file for use in OBS Studio
    if writeoutput == True:
        with open(str(maindirectory) + "/Output.txt","w") as fileoutput:
            fileoutput.write("\n" + str(message))
            fileoutput.close()
    # If platform is Mac OS or Windows, use system TTS
    if str(platform.system()) == "Darwin" or str(platform.system()) == "Windows":
        engine.say(str(message)) # System TTS [1/2]
        engine.runAndWait() # System TTS [2/2]
    else: # On Linux, use MBROLA through espeak
        # os.system("espeak -p 50 -s 165 -v mb/mb-us2 \"" + str(message) + "\"") # MBROLA TTS
        engine.say(str(message)) # System TTS [1/2]
        engine.runAndWait() # System TTS [2/2]

# Tell user that the program is starting
speaktext("The radio will be back online in a moment!")

# Start a random radio "waiting" song
sound = mixer.Sound(str(maindirectory) + "/Assets/Music/" + str(random.randint(1,radiomusiccount)) + ".WAV")
sound.set_volume(0.4)
channel = sound.play()

# State any errors/warnings to user
if weatherkey == "":
    print("You have not provided an Openweathermap API key. The API key is required to give weather info.")

# Custom function to remove unneccessary chars from YouTube video ID after "&"
def vidstrip(playlist):
    for i in range(len(playlist)):
        end=playlist[i].find("&")
        playlist[i]=playlist[i][:end]
    return playlist

# Clear url VAR
url = ""

# Set the following VARs according to the current time, for use in the IF statements below
timeobject = datetime.now()
currenttime = int(timeobject.strftime("%H"))

# Determine the weekday, then set the appropriate playlist URL and caption
# Monday
if datetime.today().weekday() == 0:
    if currenttime >= 0 and currenttime <= 8: # Early Morning [Monday]
        url = "https://www.youtube.com/playlist?list=PLjzeyhEA84sQKuXp-rpM1dFuL2aQM_a3S" # Set playlist URL
        print("Using playlist for Monday.") # Print current weekday to stdout
        weekdaytext = "Well, it's Monday. Why are you up so early? We're playing rock music all day! Let's start off your early morning with some blues music." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Early Morning"

    if currenttime > 8 and currenttime <= 12: # Morning [Monday]
        url = "https://www.youtube.com/playlist?list=PLOci2rRb5g3iUxFh_olD0dWGpzWPwdlOi" # Set playlist URL
        print("Using playlist for Monday.") # Print current weekday to stdout
        weekdaytext = "Well, it's Monday morning. We're playing rock music all day! Let's get your day started with some punk rock." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Morning"

    if currenttime > 12 and currenttime <= 16: # Afternoon [Monday]
        url = "https://www.youtube.com/playlist?list=PLGBuKfnErZlD_VXiQ8dkn6wdEYHbC3u0i" # Set playlist URL
        print("Using playlist for Monday.") # Print current weekday to stdout
        weekdaytext = "Hope you're having a solid Monday afternoon. We're playing rock music all day! Let's get the blood pumping with some heavy metal." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Afternoon"

    if currenttime > 16 and currenttime <= 20: # Evening [Monday]
        url = "https://www.youtube.com/playlist?list=PLNxOe-buLm6cz8UQ-hyG1nm3RTNBUBv3K" # Set playlist URL
        print("Using playlist for Monday.") # Print current weekday to stdout
        weekdaytext = "It's Monday evening. We're playing rock music all day! Here's some classics that you should be familiar with." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Evening"
    
    if currenttime > 20 and currenttime <= 24: # Late Night [Monday]
        url = "https://www.youtube.com/playlist?list=PL4033C6D21D7D28AC" # Set playlist URL
        print("Using playlist for Monday.") # Print current weekday to stdout
        weekdaytext = "It's Monday night. Let's end the day the right way with some death metal." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Late Night"

# Tuesday
elif datetime.today().weekday() == 1:
    if currenttime >= 0 and currenttime <= 8: # Early Morning [Tuesday]
        url = "https://www.youtube.com/playlist?list=PLwIEpqpG3Tr8aI2HwnT1YwNtDMVKf8KUO" # Set playlist URL
        print("Using playlist for Tuesday.") # Print current weekday to stdout
        weekdaytext = "It's officially Tuesday. Today, we're focusing on comedy, parodies, and generally weird music! Let's start with some comedy rock." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Early Morning"

    if currenttime > 8 and currenttime <= 12: # Morning [Tuesday]
        url = "https://www.youtube.com/playlist?list=PL7IiPgV2w_VZn8EgvZR8ohux9A5uup91n" # Set playlist URL
        print("Using playlist for Tuesday.") # Print current weekday to stdout
        weekdaytext = "Its Tuesday morning. Today, we're focusing on comedy, parodies, and generally weird music! Here's some messed up music with weird edits to get you going!" # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Morning"

    if currenttime > 12 and currenttime <= 16: # Afternoon [Tuesday]
        url = "https://www.youtube.com/playlist?list=PL4722096DA7FECEFD" # Set playlist URL
        print("Using playlist for Tuesday.") # Print current weekday to stdout
        weekdaytext = "Its Tuesday afternoon. We're focusing on comedy, parodies, and generally weird music! Right now, you're listening to music parodies!" # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Afternoon"

    if currenttime > 16 and currenttime <= 20: # Evening [Tuesday]
        url = "https://www.youtube.com/playlist?list=PL0Oo37i-_yeSwK2GaYxQEAV0BsjGDM3a8" # Set playlist URL
        print("Using playlist for Tuesday.") # Print current weekday to stdout
        weekdaytext = "Its Tuesday evening. We're focusing on comedy, parodies, and generally weird music! Let's listen to some medieval folk rock." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Evening"
    
    if currenttime > 20 and currenttime <= 24: # Late Night [Tuesday]
        url = "https://www.youtube.com/playlist?list=PLhmtZUpTH9coZD4Y0XNID7tZFmLo1bytt" # Set playlist URL
        print("Using playlist for Tuesday.") # Print current weekday to stdout
        weekdaytext = "Its Tuesday night. Let's end the day of weird music with some horror country." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Late Night"

# Wednesday
elif datetime.today().weekday() == 2:
    if currenttime >= 0 and currenttime <= 8: # Early Morning [Wednesday]
        url = "https://www.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj" # Set playlist URL
        print("Using playlist for Wednesday.") # Print current weekday to stdout
        weekdaytext = "It's officially hump day. Today's theme is nostalgic music! Time for you to jam out to some recent pop hits." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Early Morning"

    if currenttime > 8 and currenttime <= 12: # Morning [Wednesday]
        url = "https://www.youtube.com/playlist?list=PL7IiPgV2w_VaEvjQ8YedFjlcGTbhCze9U" # Set playlist URL
        print("Using playlist for Wednesday.") # Print current weekday to stdout
        weekdaytext = "It's the morning of hump day. Today's theme is nostalgic music! Let's get you started with some internet classics." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Morning"

    if currenttime > 12 and currenttime <= 16: # Afternoon [Wednesday]
        url = "https://www.youtube.com/playlist?list=PL7Q2ZklqtR8B_EAUfXt5tAZkxhCApfFkL" # Set playlist URL
        print("Using playlist for Wednesday.") # Print current weekday to stdout
        weekdaytext = "It's Wednesday afternoon. You've made it over the hump of hump day! Today's theme is nostalgic music, and we're listening to music around 2010." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Afternoon"

    if currenttime > 16 and currenttime <= 20: # Evening [Wednesday]
        url = "https://www.youtube.com/playlist?list=PLpuDUpB0osJmZQ0a3n6imXirSu0QAZIqF" # Set playlist URL
        print("Using playlist for Wednesday.") # Print current weekday to stdout
        weekdaytext = "It's Wednesday night. The theme is nostalgic music. We'll go further back in time and listen to music from the 2000s." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Evening"
    
    if currenttime > 20 and currenttime <= 24: # Late Night [Wednesday]
        url = "https://www.youtube.com/playlist?list=PLetgZKHHaF-Zq1Abh-ZGC4liPd_CV3Uo4" # Set playlist URL
        print("Using playlist for Wednesday.") # Print current weekday to stdout
        weekdaytext = "It's Wednesday night. Let's end the day with some hip hop and rap." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Late Night"

# Thursday
elif datetime.today().weekday() == 3:
    if currenttime >= 0 and currenttime <= 8: # Early Morning [Thursday]
        url = "https://www.youtube.com/playlist?list=PL4QNnZJr8sRNKjKzArmzTBAlNYBDN2h-J" # Set playlist URL
        print("Using playlist for Thursday.") # Print current weekday to stdout
        weekdaytext = "It's now Thursday morning, and early at that. Today we're focusing on music from around the world. Let's start with some K pop." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Early Morning"

    if currenttime > 8 and currenttime <= 12: # Morning [Thursday]
        url = "https://www.youtube.com/playlist?list=PLV9du90-nOngPg_V4By29gvrovqAguGuN" # Set playlist URL
        print("Using playlist for Thursday.") # Print current weekday to stdout
        weekdaytext = "It's Thursday morning. Today we're focusing on music from around the world. You're about to hear country anthems and world propaganda." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Morning"

    if currenttime > 12 and currenttime <= 16: # Afternoon [Thursday]
        url = "https://www.youtube.com/playlist?list=PLZ6V4Rz0ltCP6yVKO390YPqqfjWsgrq_n" # Set playlist URL
        print("Using playlist for Thursday.") # Print current weekday to stdout
        weekdaytext = "Thursday afternoon. We're focusing on music from around the world. Let's take a trip to India." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Afternoon"

    if currenttime > 16 and currenttime <= 20: # Evening [Thursday]
        url = "https://www.youtube.com/playlist?list=PLX9U3Rv7Wy7Wbi3iV2uxFo8BOVHjIehUc" # Set playlist URL
        print("Using playlist for Thursday.") # Print current weekday to stdout
        weekdaytext = "It's Thursday evening. We're focusing on music from around the world. Now, let's take a trip to Africa." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Evening"
    
    if currenttime > 20 and currenttime <= 24: # Late Night [Thursday]
        url = "https://www.youtube.com/playlist?list=PLrZlOVu0fKqHo1ilGq8vYCuC7mUWej_nP" # Set playlist URL
        print("Using playlist for Thursday.") # Print current weekday to stdout
        weekdaytext = "It's Thursday night. Let's end our world music theme with some American patriotic music." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Late Night"

# Friday
elif datetime.today().weekday() == 4:
    if currenttime >= 0 and currenttime <= 8: # Early Morning [Friday]
        url = "https://www.youtube.com/playlist?list=PLCD0445C57F2B7F41" # Set playlist URL
        print("Using playlist for Friday.") # Print current weekday to stdout
        weekdaytext = "It's early Friday morning. Today's decade day! We'll start by listening to the best of the eighties." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Early Morning"

    if currenttime > 8 and currenttime <= 12: # Morning [Friday]
        url = "https://www.youtube.com/playlist?list=PLGBuKfnErZlAkaUUy57-mR97f8SBgMNHh" # Set playlist URL
        print("Using playlist for Friday.") # Print current weekday to stdout
        weekdaytext = "Friday is here. Today's decade day! Next, we'll hear the best of the seventies." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Morning"

    if currenttime > 12 and currenttime <= 16: # Afternoon [Friday]
        url = "https://www.youtube.com/playlist?list=PLGBuKfnErZlCkRRgt06em8nbXvcV5Sae7" # Set playlist URL
        print("Using playlist for Friday.") # Print current weekday to stdout
        weekdaytext = "It's Friday afternoon. Today's decade day! We're moving on to the best of the sixties." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Afternoon"

    if currenttime > 16 and currenttime <= 20: # Evening [Friday]
        url = "https://www.youtube.com/playlist?list=PLRZlMhcYkA2Fhwg-NxJewUIgm01o9fzwB" # Set playlist URL
        print("Using playlist for Friday.") # Print current weekday to stdout
        weekdaytext = "It's Friday evening. Today's decade day! Let's listen to the best of the 40s!" # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Evening"
    
    if currenttime > 20 and currenttime <= 24: # Late Night [Friday]
        url = "https://www.youtube.com/playlist?list=PLXRivw5Pd9qlM5efsL4c7js8teYFVy3Dk" # Set playlist URL
        print("Using playlist for Friday.") # Print current weekday to stdout
        weekdaytext = "It's Friday night. Let's end the day with music from the roaring twenties!" # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Late Night"

# Saturday
elif datetime.today().weekday() == 5:
    if currenttime >= 0 and currenttime <= 8: # Early Morning [Saturday]
        url = "https://www.youtube.com/playlist?list=PLxvodScTx2RtAOoajGSu6ad4p8P8uXKQk" # Set playlist URL
        print("Using playlist for Saturday.") # Print current weekday to stdout
        weekdaytext = "Today's Saturday, time to relax and have fun! We'll start the morning with some orchestral music." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Early Morning"

    if currenttime > 8 and currenttime <= 12: # Morning [Saturday]
        url = "https://www.youtube.com/playlist?list=PLrnb8c3hFJatjyJ-wFMuFGANNoo7-LZsG" # Set playlist URL
        print("Using playlist for Saturday.") # Print current weekday to stdout
        weekdaytext = "Today's Saturday, time to relax and have fun! Let your morning begin with popular video game soundtracks." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Morning"

    if currenttime > 12 and currenttime <= 16: # Afternoon [Saturday]
        url = "https://www.youtube.com/playlist?list=PL4BrNFx1j7E5qDxSPIkeXgBqX0J7WaB2a" # Set playlist URL
        print("Using playlist for Saturday.") # Print current weekday to stdout
        weekdaytext = "Today's Saturday, time to relax and have fun! Let's continue your afternoon with some film scores!" # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Afternoon"

    if currenttime > 16 and currenttime <= 20: # Evening [Saturday]
        url = "https://www.youtube.com/playlist?list=PL6rfTXx-6y2U9LPalxmyWb4Z9_YDomxfs" # Set playlist URL
        print("Using playlist for Saturday.") # Print current weekday to stdout
        weekdaytext = "Today's Saturday, time to relax and have fun! Now that it's the evening, we'll listen to songs in musical theater." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Evening"
    
    if currenttime > 20 and currenttime <= 24: # Late Night [Saturday]
        url = "https://www.youtube.com/playlist?list=PLbcjjn493-S_DcwEVTPkVRz5zZQSo3hjE" # Set playlist URL
        print("Using playlist for Saturday.") # Print current weekday to stdout
        weekdaytext = "It's Saturday night, still time to relax and have fun! We'll end the day with some pirate metal." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Late Night"

# Sunday
elif datetime.today().weekday() == 6:
    if currenttime >= 0 and currenttime <= 8: # Early Morning [Sunday]
        url = "https://www.youtube.com/playlist?list=PLWtAfhR9YD1wdKOTDqCFYoFUcThRCfAjp" # Set playlist URL
        print("Using playlist for Sunday.") # Print current weekday to stdout
        weekdaytext = "It's Sunday. We're serving jazz all day baby. Smooth jazz will be deployed in 3, 2, 1." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Early Morning"

    if currenttime > 8 and currenttime <= 12: # Morning [Sunday]
        url = "https://www.youtube.com/playlist?list=PL8F6B0753B2CCA128" # Set playlist URL
        print("Using playlist for Sunday.") # Print current weekday to stdout
        weekdaytext = "It's Sunday morning. We're serving jazz all day baby. Let's start your morning by listening to important figures in jazz." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Morning"

    if currenttime > 12 and currenttime <= 16: # Afternoon [Sunday]
        url = "https://www.youtube.com/playlist?list=PLDC827E741DA933F0" # Set playlist URL
        print("Using playlist for Sunday.") # Print current weekday to stdout
        weekdaytext = "It's Sunday afternoon. We're serving jazz all day baby. Time to get moving to some big band music." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Afternoon"

    if currenttime > 16 and currenttime <= 20: # Evening [Sunday]
        url = "https://www.youtube.com/playlist?list=PLk-_AvR22RueziRgt5GVuirih223y1UNJ" # Set playlist URL
        print("Using playlist for Sunday.") # Print current weekday to stdout
        weekdaytext = "It's Sunday evening. We're serving jazz all day baby. Let's cool down to some bossa nova." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Evening"
    
    if currenttime > 20 and currenttime <= 24: # Late Night [Sunday]
        url = "https://www.youtube.com/playlist?list=PL3O5lr1JOzLe6CXisC7PSbveY6IBLxdlg" # Set playlist URL
        print("Using playlist for Sunday.") # Print current weekday to stdout
        weekdaytext = "It's Sunday night. Let's end the day with some jazz fusion." # Set speech text according to weekday
        savedweekday = datetime.today().weekday()
        savedtime = "Late Night"

# If the playlist URL is still blank, warn the user and use a fallback playlist
if url == "":
    url = "https://www.youtube.com/playlist?list=PLHL1i3oc4p0o76QOZ_BLZwjDb1x21azmC"
    print("You didn't specify a music playlist for today's date! Using fallback playlist.")

# If specified, override the weekday playlist with something else
if overrideplaylist:
    url = overrideplaylist
    print("Override enabled for playlist. Using " + str(url) + ".")

# Print steps to stdout
print("Scraping music playlist ...")

# Set Firefox to run in headless mode
opts = FirefoxOptions()
opts.add_argument("--headless")
driver = webdriver.Firefox(options=opts)

# Open playlist URL in headless Firefox
driver.get(url)

# Declare lists for playlist video URLs and titles
playlist=[]
playlistnames=[]

videos=driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')

# Scrape each video into two lists, video URLs and video titles respectively
for video in videos:
    link=video.find_element_by_xpath('.//*[@id="video-title"]').get_attribute("href")
    name=video.find_element_by_xpath('.//*[@id="video-title"]').get_attribute("title")
    playlist.append(link)
    playlistnames.append(name)

musicplaylist=vidstrip(playlist) # Strip unneccessary chars from list
driver.close() # Close the web rendering engine

# Print message to stdout
print("Finished downloading music playlist.")

# Next, scrape the PSA playlist (if playlist URL is specified)
if psaplaylisturl != "":
    # Set URL for PSAs instead of music
    url = psaplaylisturl

    # Print steps to stdout
    print("Scraping PSA playlist ...")

    # Run Firefox in automated headless mode
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)
    driver.get(url) # Open URL
    playlist=[] # Clear "playlist" list

    videos=driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')
    for video in videos:
        link2=video.find_element_by_xpath('.//*[@id="video-title"]').get_attribute("href")
        playlist.append(link2) # Append each URL to the list

    psaplaylist=vidstrip(playlist)
    driver.close() # Close the web rendering engine
else:
    # Print missing playlist info message to stdout
    print("PSA playlist URL has not been set. The station will not play PSAs.")

# Print completion message to stdout
print("Finished downloading PSA playlist. Starting radio ...")

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
longspeechstring += "\n" + str(speechIntroTextShort[random.randint(0,len(speechIntroTextShort)-1)])
longspeechstring += " Version " + str(versioninfo) + "."

# Add a random variation of the "First Run Prompts" speech to longspeechstring var
longspeechstring += "\n" + str(speechFirstrunPrompts[random.randint(0,len(speechFirstrunPrompts)-1)])

# If advancedspeech option is enabled,
if advancedspeech == True:
    speaktext("Almost there. Just a few more seconds while speech is being generated.")
    preparevoice(longspeechstring) # Trigger voice synthesis engine for generation
    speakrichtext(longspeechstring) # Trigger voice synthesis engine for playback

sound.stop()

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
                sound.set_volume(0.5)
                channel = sound.play()
                while channel.get_busy():
                    pygame.time.wait(100)
            
            # Play the synthesized voice if enabled, else use system TTS
            if advancedspeech == True:
                sound = mixer.Sound(str(maindirectory) + "/Output.wav")
                sound.set_volume(1)
                channel = sound.play()
                while channel.get_busy():
                    pygame.time.wait(100)
            else:
                speaktext(longspeechstring)

            # Play random radio sound after speaking (if file exists)
            if radiosoundcount >= 1:
                sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects/" + str(random.randint(1,radiosoundcount)) + ".WAV")
                sound.set_volume(0.5)
                channel = sound.play()
                while channel.get_busy():
                    pygame.time.wait(100)

            # Choose the first song to play
            if len(listPlayedSongs) >= len(musicplaylist) - 1: # If the music list has been exhausted
                listPlayedSongs.clear() # Clear the list and start again
            potentialsong = random.randint(1,len(musicplaylist)-1) # Choose a random song index from the playlist
            while potentialsong in listPlayedSongs: # If the song has been chosen already,
                potentialsong = random.randint(1,len(musicplaylist)-1) # Randomly select a new song from the playlist
            listPlayedSongs.append(potentialsong) # Add the song index to the list of played songs
            songselectionint = potentialsong # Set the next song to the one that was randomly chosen
            print("Songs played: (Includes upcoming song) " + str(listPlayedSongs)) # Show list of played song numbers
            print("Likelihood VARs:\nPSA: " + str(psachance) + "\nWeather: " + str(weatherchance) + "\nWelcomeMessage: " + str(welcomechance) + "\nWeekdayMessage: " + str(weekdaychance) + "\nTime: " + str(timechance)) # Show chance VARs

            longspeechstring = "" # Clear the longspeechstring var
            if advancedspeech: # If advanced speech is enabled,
                longspeechstring += "Announcer two here. " # Add the text "announcer two here" to longspeechstring var
            longspeechstring += "\n" + str(speechSongTransitions[random.randint(0,len(speechSongTransitions)-1)]) + str(playlistnames[songselectionint]) + "."
            # longspeechstring += "\n" + str(speechSongTransitions[random.randint(0,len(speechSongTransitions)-1)]) + str(playlistnames[songselectionint]) + "."
            
            # Chance to speak "Stay safe out there!"
            if random.randint(0,4) == 1:
                longspeechstring += " Stay safe out there!"
            
            # Use system TTS engine to speak the next song info
            speaktext(longspeechstring)

            # Prevent the intro from playing again on next loop
            playintro = False

        # [ [ [ CURRENTLY NOT WORKING ] ] ]
        # If writesonginfo is enabled, write the song title to SongInfo.txt
        # if writesonginfo == True:
        #     with open(str(maindirectory) + "/SongInfo.txt","w") as fileoutput2:
        #         fileoutput2.write(str(playlistnames[songselectionint])
        #         fileoutput2.close()

        # Download the next song with pafy module
        url = musicplaylist[songselectionint]
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url

        # Play the downloaded song in headless VLC
        Instance = vlc.Instance("--vout=dummy")
        player = Instance.media_player_new()
        Media = Instance.media_new(playurl)
        Media.get_mrl()
        player.set_media(Media)
        player.play()
        player.audio_set_volume(80)

        # Clear the longspeechstring var
        longspeechstring = ""

        # Song that just played
        longspeechstring += str(speechSongEndTransitions[random.randint(0,len(speechSongEndTransitions)-1)]) + str(playlistnames[songselectionint]) + "."

        # Listening to PhysCorp's Automated Station & Version Info
        longspeechstring += "\n" + str(speechIntroTextShort[random.randint(0,len(speechIntroTextShort)-1)])
        longspeechstring += " Version " + str(versioninfo) + "."

        # # Chance to mention the time
        # if random.randint(0, timechance) == 1:
        #     timeobject = datetime.now()
        #     currenttime = timeobject.strftime("%I:%M")
        #     longspeechstring += "\nThe time is currently " + str(currenttime) + "."
        #     timechance = defaulttimechance

        # # Increase the chance to speak the time
        # if timechance > 2:
        #     timechance -= 1

        # Chance to mention one of the "First Run Prompts" again
        if random.randint(0, welcomechance) == 1:
            # Add a random variation of the "First Run Prompts" speech to longspeechstring var
            longspeechstring += "\nIf you just tuned in, " + str(speechFirstrunPrompts[random.randint(0,len(speechFirstrunPrompts)-1)])
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
                print("A city name has not been set. Using Auburn Hills.")

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
                longspeechstring += "\nLet's check up on the weather outside! Here in " + str(city_name) + ", current conditions are " + str(weather_description) + ", and the temperature is " + str(round(current_temperature)) + " degrees."

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
        print("Songs played: (Includes upcoming song) " + str(listPlayedSongs)) # Show list of played song numbers
        print("Likelihood VARs:\nPSA: " + str(psachance) + "\nWeather: " + str(weatherchance) + "\nWelcomeMessage: " + str(welcomechance) + "\nWeekdayMessage: " + str(weekdaychance) + "\nTime: " + str(timechance)) # Show chance VARs
        
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
        # longspeechstring += "\n" + str(speechSongTransitions[random.randint(0,len(speechSongTransitions)-1)]) + str(playlistnames[songselectionint]) + "."
        longspeechstring += "\n" + str(speechSongTransitions[random.randint(0,len(speechSongTransitions)-1)]) + str(playlistnames[songselectionint]) + "."

        # Chance to play a PSA
        if random.randint(0,psachance) == 1 and psaplaylisturl != "":
            playpsa = True
            longspeechstring += "\nBut first. A message from our sponsors. Don't touch that dial."
            # Reset psachance var
            psachance = defaultpsachance

        # Chance to include "Stay safe out there!" in speech
        if random.randint(0,4) == 1:
            longspeechstring += "\nStay safe out there!"

        # Prepare the synthesized speech if enabled
        if advancedspeech == True:
            preparevoice(longspeechstring)

        # Wait until music finishes playing on VLC
        time.sleep(1.5)
        duration = player.get_length() / 1000
        time.sleep(duration)
        player.stop()
        player.release()
        Media.release()
        Instance.release()

        # Play random radio sound before speaking if file exists
        if radiosoundcount >= 1:
            sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects/" + str(random.randint(1,radiosoundcount)) + ".WAV")
            sound.set_volume(0.5)
            channel = sound.play()
            while channel.get_busy():
                pygame.time.wait(100)
        
        # If the time is midnight (if stored weekday info doesn't match current weekday info), restart the script to gather new playlist info
        if savedweekday != datetime.today().weekday():
            speaktext("It's midnight. I'm switching to a new playlist. Please wait.")
            os.execv(sys.executable, ['python3'] + sys.argv) # Restart the script by issuing a terminal command
        
        # Compared the savedtime VAR to the current time text. If mismatch, restart the station with a new playlist
        timeobject = datetime.now()
        currenttime = int(timeobject.strftime("%H"))

        if currenttime >= 0 and currenttime <= 8: # Early Morning
            savedtimecomparison = "Early Morning"

        elif currenttime > 8 and currenttime <= 12: # Morning
            savedtimecomparison = "Morning"

        elif currenttime > 12 and currenttime <= 16: # Afternoon
            savedtimecomparison = "Afternoon"

        elif currenttime > 16 and currenttime <= 20: # Evening
            savedtimecomparison = "Evening"
        
        elif currenttime > 20 and currenttime <= 24: # Late Night
            savedtimecomparison = "Late Night"
        
        # If mismatch, restart the station
        if savedtimecomparison != savedtime:
            speaktext("I'm switching to a new playlist. Please wait.")
            os.execv(sys.executable, ['python3'] + sys.argv) # Restart the script by issuing a terminal command

        # Play the synthesized speech, or use fallback TTS if not ready
        if advancedspeech == True:
            speakrichtext(longspeechstring)
        else:
            speaktext(longspeechstring)

        # Play the PSA if triggered
        if playpsa == True:
            playpsa = False # Prevent PSA from running twice
            
            # Play the PSA, if the video isn't available, repeat the process until one is
            while True:
                try:
                    # Play PSA using headless VLC
                    url = psaplaylist[random.randint(1,len(psaplaylist)-1)]
                    video = pafy.new(url)
                    best = video.getbest()
                    playurl = best.url

                    Instance = vlc.Instance("--vout=dummy")
                    player = Instance.media_player_new()
                    Media = Instance.media_new(playurl)
                    Media.get_mrl()
                    player.set_media(Media)
                    player.play()
                    player.audio_set_volume(70)

                    time.sleep(1.5)
                    duration = player.get_length() / 1000
                    time.sleep(duration)
                    player.stop()
                    player.release()
                    Media.release()
                    Instance.release()
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
            sound.set_volume(0.5)
            channel = sound.play()
            while channel.get_busy():
                pygame.time.wait(100)
    except (RuntimeError, TypeError, NameError, OSError):
        # Say that something has gone wrong
        speaktext("It looks like that song isn't available. Please wait while I restart the station.")
        os.execv(sys.executable, ['python3'] + sys.argv) # Restart the script by issuing a terminal command