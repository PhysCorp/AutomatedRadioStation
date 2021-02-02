# Import Modules
import random # Random number generation
import pyttsx3 # Fallback text to speech
import pafy # Video downloading
import vlc # Play music and videos
import time # Sleep and wait commands
# import subprocess # Run commands in parallel
import datetime # Tell the date on air, as well as determine which playlist based on weekday
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
#engine.setProperty('rate', 125) # Speech rate
engine.setProperty('volume',1.0) # Speech volume

# Init random numbers
random.seed(a=None, version=2) # Set random seed based on current time

# Init audio engine
mixer = pygame.mixer
mixer.init()

# Declare Variables
longspeechstring = "" # Used to append multiple strings before synthesizing audio
playpsa = False # Bool value for whether or not a PSA will play immediately following a song
listPlayedSongs = [] # List stores all song numbers that have already been played
potentialsong = 1 # The index of the song to be played
maindirectory = os.path.dirname(__file__) # The absolute path to this file

# Options
playintro = True # Play the radio show intro upon first launch
advancedspeech = False # Use AI-based speech generation service
psachance = 10 # Likelihood of playing a PSA [1/[x] chance]
weatherchance = 10 # Likelihood of mentioning the weather [1/[x] chance]
welcomechance = 10 # Likelihood of mentioning the welcome message again [1/[x] chance]
weekdaychance = 10 # Likelihood of mentioning the weekday again [1/[x] chance]
weatherkey = "" # API key for Openweathermap
overrideplaylist = "" # Override YouTube playlist URL

# Init radio sounds (The number of available radio sounds to be played)
DIR= os.path.join(maindirectory,"Assets/SoundEffects")
radiosoundcount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

# Custom function to speak with my AI generated voice
def playvoice(message):
    os.system("python3 \"" + str(maindirectory) + "/Real-Time-Voice-Cloning-master/demo_cli.py\" --no_sound --speechcontent \"" + str(re.sub("[\W ]+"," ",str(message).replace(".","_")).replace("_",". ")) + "\"")
    print(str(message)) # Display output in stdout
    # Write message contents to text file for use in OBS Studio
    with open(str(maindirectory) + "/Output.txt","w") as fileoutput:
        fileoutput.write("\n" + str(message))
        fileoutput.close()
    longspeechstring = "" # Clear longspeechstring var

# Custom function to synthesize audio in the background [followed by speakrichtext function]
def preparevoice(message):
    if path.exists(str(maindirectory) + "/Output.wav"): # If the old file exists already
        if str(platform.system()) == "Darwin" or str(platform.system()) == "Linux":
            os.system("rm \"" + str(maindirectory) + "/Output.wav" + "\"") # Delete the old file [Linux and Mac OS]
        else:
            os.system("del \"" + str(maindirectory) + "/Output.wav" + "\"") # Delete the old file [Windows]
    # Run the neural synthesis engine asynchronously, piping all output to nohup.out
    os.system("nohup python3 \"" + str(maindirectory) + "/Real-Time-Voice-Cloning-master/demo_cli.py\" --no_sound --speechcontent \"" + str(re.sub("[\W ]+"," ",str(message).replace(".","_")).replace("_",". ")) + "\"  &")

# Speak text with neural synthesis engine first, but fallback to espeak TTS if the file isn't ready
def speakrichtext(message):
    # Write message contents to text file for use in OBS Studio
    with open(str(maindirectory) + "/Output.txt","w") as fileoutput:
        fileoutput.write("\n" + str(message))
        fileoutput.close()
    # If the file is not ready, use fallback TTS, prepending string with "Announcer two here."
    if path.exists(str(maindirectory) + "/Output.wav") is False:
        speaktext("Announcer two here. " + str(message))
    else: # If the file IS ready, play it synchronously
        sound = mixer.Sound(str(maindirectory) + "/Output.wav")
        sound.set_volume(1)
        channel = sound.play()
        while channel.get_busy():
            pygame.time.wait(100)
    longspeechstring = "" # Clear longspeechstring var

# Custom function to just speak text with espeak
def speaktext(message):
    print(str(message)) # Print the message contents to stdout
    # Write message contents to text file for use in OBS Studio
    with open(str(maindirectory) + "/Output.txt","w") as fileoutput:
        fileoutput.write("\n" + str(message))
        fileoutput.close()
    engine.say(str(message))
    engine.runAndWait()


# Tell user that the program is starting
speaktext("The radio will be back online in a moment!")

# State any errors/warnings to user
if weatherkey == "":
    print("You have not provided an Openweathermap API key. The API key is required to give weather info.")

# Scrape the appropriate playlist for songs
def vidstrip(playlist):
    for i in range(len(playlist)):
        end=playlist[i].find("&") # Remove unneccessary chars from YouTube video ID
        playlist[i]=playlist[i][:end]
    return playlist

# DO SWITCH STATEMENTS EXIST IN PYTHON??? No.

# Determine the weekday, then set the appropriate playlist
if datetime.datetime.today().weekday() == 0: # Monday
    url = "https://www.youtube.com/playlist?list=PLNxOe-buLm6cz8UQ-hyG1nm3RTNBUBv3K" # Set playlist URL
    print("Using playlist for Monday.") # Print current weekday to stdout
    weekdaytext = "Well its Monday. Here's some rock music to get you going." # Set speech text according to weekday
    savedweekday = datetime.datetime.today().weekday()

elif datetime.datetime.today().weekday() == 1: # Tuesday
    url = "https://www.youtube.com/playlist?list=PL7IiPgV2w_VZn8EgvZR8ohux9A5uup91n" # Set playlist URL
    print("Using playlist for Tuesday.") # Print current weekday to stdout
    weekdaytext = "Its Tuesday. Today we're serving up some messed up music." # Set speech text according to weekday
    savedweekday = datetime.datetime.today().weekday()

elif datetime.datetime.today().weekday() == 2: # Wednesday
    url = "https://www.youtube.com/playlist?list=PL7IiPgV2w_VaEvjQ8YedFjlcGTbhCze9U" # Set playlist URL
    print("Using playlist for Wednesday.") # Print current weekday to stdout
    weekdaytext = "Its officially hump day. Time to throw you for a loop with some nostalgia." # Set speech text according to weekday
    savedweekday = datetime.datetime.today().weekday()

elif datetime.datetime.today().weekday() == 3: # Thursday
    url = "https://www.youtube.com/playlist?list=PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10" # Set playlist URL
    print("Using playlist for Thursday.") # Print current weekday to stdout
    weekdaytext = "Thursday. The perfect time for pop hits." # Set speech text according to weekday
    savedweekday = datetime.datetime.today().weekday()

elif datetime.datetime.today().weekday() == 4: # Friday
    url = "https://www.youtube.com/playlist?list=PL7IiPgV2w_VZn8EgvZR8ohux9A5uup91n" # Set playlist URL
    print("Using playlist for Friday.") # Print current weekday to stdout
    weekdaytext = "Friday is here. Let's listen to some messed up music." # Set speech text according to weekday
    savedweekday = datetime.datetime.today().weekday()

elif datetime.datetime.today().weekday() == 5: # Saturday
    url = "https://www.youtube.com/playlist?list=PLGBuKfnErZlAkaUUy57-mR97f8SBgMNHh" # Set playlist URL
    print("Using playlist for Saturday.") # Print current weekday to stdout
    weekdaytext = "Todays Saturday. You know what that means. Seventies hits all day baby." # Set speech text according to weekday
    savedweekday = datetime.datetime.today().weekday()

elif datetime.datetime.today().weekday() == 6: # Sunday
    url = "https://www.youtube.com/playlist?list=PLWtAfhR9YD1wdKOTDqCFYoFUcThRCfAjp" # Set playlist URL
    print("Using playlist for Sunday.") # Print current weekday to stdout
    weekdaytext = "Its Sunday. Time to chill out to some smooth jazz." # Set speech text according to weekday
    savedweekday = datetime.datetime.today().weekday()

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

# speaktext("Successfully downloaded music list.")

# Scrape the PSA playlist
def vidstrip(playlist):
    for i in range(len(playlist)):
        end=playlist[i].find("&") # Remove unneccessary chars from list
        playlist[i]=playlist[i][:end]
    return playlist

# Set URL for PSAs
url = "https://www.youtube.com/playlist?list=PL7IiPgV2w_VZg0cfEt4uOBqSpPevxmV3C"

# Print steps to stdout
print("Scraping PSA playlist ...")

# Run Firefox in automated headless mode
opts = FirefoxOptions()
opts.add_argument("--headless")
driver = webdriver.Firefox(options=opts)
driver.get(url) # Open URL
playlist=[] # Clear playlist

videos=driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')
for video in videos:
    link2=video.find_element_by_xpath('.//*[@id="video-title"]').get_attribute("href")
    playlist.append(link2) # Append each URL to the list

psaplaylist=vidstrip(playlist)
driver.close() # Close the web rendering engine

# Print steps to stdout
print("Done.")

# Read and store each external speech script into memory
# (Each line in the textfile represents a different index in the list)

# Intro Text Short
fileIntroTextShort = open(str(maindirectory) + "/SpeechScripts/IntroTextShort.txt", "r")
speechIntroTextShort = fileIntroTextShort.readlines()
fileIntroTextShort.close()

# First Run Prompts
fileFirstrunPrompts = open(str(maindirectory) + "/SpeechScripts/FirstrunPrompts.txt", "r")
speechFirstrunPrompts = fileFirstrunPrompts.readlines()
fileFirstrunPrompts.close()

# Prepare the intro lines with synthesized voice
longspeechstring = "" # Clear the longspeechstring var

# If the playlist isn't overridden, add the weekday text to longspeechstring var
if not overrideplaylist:
    longspeechstring += str(weekdaytext)

# Add a random variation of the "Intro Text Short" speech to longspeechstring var
longspeechstring += "\n" + str(speechIntroTextShort[random.randint(0,len(speechIntroTextShort)-1)])

# Add a random variation of the "First Run Prompts" speech to longspeechstring var
longspeechstring += "\n" + str(speechFirstrunPrompts[random.randint(0,len(speechFirstrunPrompts)-1)])

# If advancedspeech option is enabled,
if advancedspeech == True:
    speaktext("Almost there. Just a few more seconds while speech is being generated.")
    playvoice(longspeechstring) # Trigger voice synthesis engine for generation and playback

# Loop through songs, announcements, and other commentary forever
while True:
    try:
        # Set the random seed again based on current time
        random.seed(a=None, version=2)
        
        # Play radio intro if enabled
        if playintro == True:
            # Play random radio sound before speaking if file exists
            if radiosoundcount >= 1:
                sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects/" + str(random.randint(1,radiosoundcount - 1)) + ".WAV")
                sound.set_volume(0.5)
                channel = sound.play()
                while channel.get_busy():
                    pygame.time.wait(100)
            
            # Play the synthesized voice if enabled
            if advancedspeech == True:
                sound = mixer.Sound(str(maindirectory) + "/Output.wav")
                sound.set_volume(1)
                channel = sound.play()
                while channel.get_busy():
                    pygame.time.wait(100)
            else:
                speaktext(longspeechstring)

            # Play random radio sound after speaking if file exists
            if radiosoundcount >= 1:
                sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects/" + str(random.randint(1,radiosoundcount - 1)) + ".WAV")
                sound.set_volume(0.5)
                channel = sound.play()
                while channel.get_busy():
                    pygame.time.wait(100)

            # Choose the first song with announcer two
            if len(listPlayedSongs) >= len(musicplaylist) - 1: # If the music list has been exhausted
                listPlayedSongs.clear() # Clear the list and start again
            
            potentialsong = random.randint(1,len(musicplaylist)-1) # Choose a random song index from the playlist
            while potentialsong in listPlayedSongs: # If the song has been chosen already,
                potentialsong = random.randint(1,len(musicplaylist)-1) # Randomly select a new song from the playlist
            listPlayedSongs.append(potentialsong) # Add the song index to the list of played songs
            songselectionint = potentialsong # Set the next song to the one that was randomly chosen
            print("Songs played: (Includes upcoming song) " + str(listPlayedSongs)) # Show list of played song numbers

            longspeechstring = "" # Clear the longspeechstring var
            if advancedspeech: # If advanced speech is enabled,
                longspeechstring += "Announcer two here. " # Add the text "announcer two here" to longspeechstring var
            longspeechstring += "Up next is " + str(playlistnames[songselectionint]) + "."
            
            # Chance to speak "Stay safe out there!"
            if random.randint(0,4) == 1:
                longspeechstring += " Stay safe out there!"
            
            # Use espeak engine to speak the next song
            speaktext(longspeechstring)

            # Prevent the intro from playing again
            playintro = False

        # Download the next song with pafy
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
        longspeechstring += "That was " + str(playlistnames[songselectionint]) + "."

        # Listening to W X O U
        longspeechstring += "\n" + str(speechIntroTextShort[random.randint(0,len(speechIntroTextShort)-1)])

        # Chance to mention one of the "First Run Prompts" again
        if random.randint(0, welcomechance) == 1:
            # Add a random variation of the "First Run Prompts" speech to longspeechstring var
            longspeechstring += "\nIf you just tuned in, " + str(speechFirstrunPrompts[random.randint(0,len(speechFirstrunPrompts)-1)])

        # Increase the chance to speak the welcome message
        if welcomechance > 2:
            welcomechance -= 1

        # Chance to talk about the weather [copied from online tutorial]
        if random.randint(0,weatherchance) == 1 and weatherkey != "":
            weatherchance = 6
            # Talk about weather using Openweathermap API

            # My API key
            api_key = weatherkey

            # base_url variable to store the Openweathermap URL 
            base_url = "http://api.openweathermap.org/data/2.5/weather?"

            # Set city name
            city_name = "Auburn Hills"

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
                # to the "pressure" key of y 
                current_pressure = y["pressure"] 

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
                longspeechstring += "\nLet's check up on the weather outside! Current conditions outside are " + str(weather_description) + ", and the temperature is " + str(round(current_temperature)) + " degrees."

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
        
        # If the playlist isn't overridden, chance to add the weekday text to longspeechstring var
        if not overrideplaylist:
            if random.randint(0,weekdaychance) == 1:
                longspeechstring += " " + str(weekdaytext)
            # Increase the chance to speak the current weekday
            if weekdaychance > 2:
                weekdaychance -= 1

        # Add the next song info to the longspeechstring var
        longspeechstring += "\nUp next is " + str(playlistnames[songselectionint]) + "."

        # Chance to play a PSA
        if random.randint(0,psachance) == 1:
            playpsa = True
            longspeechstring += "\nBut first. A message from our sponsors. Don't touch that dial."

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
            sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects/" + str(random.randint(1,radiosoundcount - 1)) + ".WAV")
            sound.set_volume(0.5)
            channel = sound.play()
            while channel.get_busy():
                pygame.time.wait(100)
        
        # If the time is midnight, restart the script to gather new playlist info
        if savedweekday != datetime.datetime.today().weekday():
            speaktext("It's midnight. I'm switching to a new playlist. Please wait.")
            os.execv(sys.executable, ['python3'] + sys.argv) # Restart the script

        # Play the synthesized speech, or use fallback espeak if not ready
        if advancedspeech == True:
            speakrichtext(longspeechstring)
        else:
            speaktext(longspeechstring)

        # Play the PSA if triggered
        if playpsa == True:
            psachance = 6 # Reset PSA chance var
            playpsa = False # Prevent PSA from running twice
            
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
            player.audio_set_volume(95)

            time.sleep(1.5)
            duration = player.get_length() / 1000
            time.sleep(duration)
            player.stop()
            player.release()
            Media.release()
            Instance.release()
        
        # Increase chance to play PSA next time
        if psachance > 2:
            psachance -= 1

        # Play random radio sound after speaking if file exists
        if radiosoundcount >= 1:
            sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects/" + str(random.randint(1,radiosoundcount - 1)) + ".WAV")
            sound.set_volume(0.5)
            channel = sound.play()
            while channel.get_busy():
                pygame.time.wait(100)
    except (RuntimeError, TypeError, NameError, OSError):
        # Say that something has gone wrong
        speaktext("It looks like something has gone wrong. Please wait while I restart the station.")
        os.execv(sys.executable, ['python3'] + sys.argv) # Restart the script
