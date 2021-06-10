
# Try to import all modules
try:
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
    import requests # Gather weather info from Openweathermap
    import sys # Used to restart the script at midnight, as well as script args
    import platform # Identify which OS the script is running on
    import json # Parse JSON files for API and playlist info
    import subprocess # Run multiple processes in parallel
    import gc # Memory management for audio processing
    from dashing import * # Console dashboard. Provides pretty text output to stdout.
    # from textgenrnn import textgenrnn # AI-based text generation
    from google.cloud import texttospeech # [PAID] Google Cloud Text to Speech

    # Custom Modules
    from WeatherResponses import WeatherSpeech # Return specific sentence based on weather conditions
    from ConsoleUI import Dashboard # Custom dashboard for stdout

except ImportError:
    print("[WARN] You are missing one or more libraries. This script cannot continue.")
    print("Try running in terminal >> python3 -m pip install -r requirements.txt")
    quit()

# Custom error for a negative port number
class NegativePortNumber(Exception):
    pass

# Custom error for negative value in song length
class NegativeMaximumSongLength(Exception):
    pass

# Custom error if playlist URL is not in correct domain
class PlaylistDomainError(Exception):
    pass

# Custom error for negative value in random bounds
class NegativeRandomBounds(Exception):
    pass

class RadioHost:
    def __init__(self):
        self.helloworld = "Hello World!"
    
    def starttutorial(self):
        # Init TTS engine
        engine = pyttsx3.init()
        # engine.setProperty('rate', 185) # Set speech rate
        engine.setProperty('volume',1.0) # Set speech volume

        def speak(message):
            print("[INFO] " + str(message), end="\n\n")
            # If platform is Mac OS or Windows, use system TTS
            if str(platform.system()) == "Darwin" or str(platform.system()) == "Windows":
                engine.say(str(message)) # System TTS [1/2]
                engine.runAndWait() # System TTS [2/2]
            else: # On Linux, use espeak
                os.system("espeak \"" + str(message).replace("'","").replace("\"","") + "\"")
        
        speak("Welcome to PhysCorp's Automated Radio Station. The following prompts will help guide you through setting up this program to fit your own needs. To skip the tutorial at any time, simply restart the program. This message only plays once. If you wish to start the tutorial again, delete the file titled \"Firstrun.txt\" in the program's main directory. Let's begin! Press enter to continue.")
        try:
            dummyvalue = input("Press enter to continue.")
        except (EOFError):
            pass
        speak("First, take a look at the program's main directory. You will see several files and folders, such as \"SpeechScripts\" and \"Assets.\" Each file has a specific purpose. First, we'll start with the Assets folder.")
        try:
            dummyvalue = input("Press enter to continue.")
        except (EOFError):
            pass
        speak("The Assets folder contains any audio assets for the program. Currently, you will see one folder: SoundEffects. Inside of the SoundEffects folder, you can copy and paste an unlimited number of short WAV files here, which serve as transitions between speech and music. A random sound file plays each time. If you do not wish to have any transition sounds, leave the folder empty. Once you are ready to move on, press enter to continue.")
        try:
            dummyvalue = input("Press enter to continue.")
        except (EOFError):
            pass
        speak("Back in the main directory, we will take a look at the SpeechScripts folder. Inside of this folder, you will find four text files: FirstRunPrompts, IntroTextShort, SongEndTransitions, and SongTransitions. These files serve as pseudo-random messages that play at specific intervals of the program. Before we go further, here are the details for each of the four files. FirstrunPrompts contains all of the paragraph-length introductions for the radio show. On the other hand, IntroTextShort is a drastically shorter version of the previous file, containing small messages and reminders for listeners. SongTransitions details any transitional phrases before playing a song, while SongEndTransitions provides a brief phrase after a song has finished playback. Let's take a look at SongTransitions.txt. Each line of the text file contains a different message to be read. This program chooses a line at random and reads it to the audience. With this particular file, SongTransitions.txt, this prepends each song title with a transitional phrase, such as \"You're about to hear,\" followed by the song name. You can add an unlimited number of lines to each text file, which increases the variety of speech on air. When you have modified each of the four text files to your liking, press enter to continue.")
        try:
            dummyvalue = input("Press enter to continue.")
        except (EOFError):
            pass
        speak("Back in the main directory again, we'll take a look at several files. Let's start with \"APIKeys.json.\" This file holds the keys that this program uses to make API calls. Currently, there is only one entry: OpenWeatherMap. If you wish to hear about weather info, such as current conditions and temperature, copy and paste your OpenWeatherMap key in the double quotes in this file. If you wish to obtain a key, visit \"https://openweathermap.org/api\" for more info. When you are ready, press enter to continue.")
        try:
            dummyvalue = input("Press enter to continue.")
        except (EOFError):
            pass
        speak("Now, we'll take a look at the file titled \"GoogleAPIKey.json.\" This file holds your Google API key for use with their WaveNet voices. If you wish to use WaveNet for high quality, realistic voices, search on the internet for obtaining a Cloud Console API Key. Just letting you know, Google Cloud charges a fee per every million characters that you call. Once you have your Cloud Console Key, simply REPLACE this file with your JSON key, being sure to name the file \"GoogleAPIKey.json.\" Press enter to continue.")
        try:
            dummyvalue = input("Press enter to continue.")
        except (EOFError):
            pass
        speak("Next, we'll take a look at the Python file titled \"PlaylistSearch.py.\" Here, you can edit which playlists this program uses, as well as when the playlist should play. Around line 22 of the file, you will see several blocks of text. Self weekdaynum represents the day of the week, starting with zero being Monday and six being Sunday. Find the appropriate block of text that you wish to edit for a specific day of the week. Inside of that specific block of text, you'll see five separate playlists. These five playlists activate at specific times throughout the day, referenced by self timeofdaynum. The first link plays from midnight to 8 AM, the second from 8 to noon, the third from noon to four, the fourth from four to eight at night, and the fifth from eight to midnight of the next day. Please edit any playlist links accordingly. After you are satisfied, press enter to continue with setting appropriate playlist titles.")
        try:
            dummyvalue = input("Press enter to continue.")
        except (EOFError):
            pass
        speak("In the same file, we'll discuss setting playlist titles. Around line 107, you'll see a similar layout with each block of text, referenced by weekday and time of day. Here, each return statement is a separate line that this script reads when announcing the current playlist. For whichever playlists you modified, continue to change the text accordingly, keeping in mind the weekday and time of day numbers. When you are ready to continue, press enter.")
        try:
            dummyvalue = input("Press enter to continue.")
        except (EOFError):
            pass
        speak("Now, we're almost done. We'll take a look at the most important file, \"Options.json.\" This file contains all of the program's options. Upon opening the file in your text editor, you'll see a range of different preferences, such as suggestions and max song length. Please edit the values accordingly. I'll describe each option here first. Playintro states whether you want to have the program give its long introduction before starting song playback. Suggestions states whether you want users to visit the associated website and suggest YouTube links to songs to be played live. Normalize audio serves to make all songs the same perceived volume. This function currently causes a memory leak, but greatly improves the quality of the radio. The port option allows you to specify which port the web server will run on. Dashboard serves to beautify the terminal output when monitoring the station. Offline mode serves to limit the number of YouTube and API calls that the program makes. Max song length sets the maximum allowable length that a song can play for. This helps to prevent pesky 24 hour loop songs from taking up the radio. The next few options describe modifying the wavenet voice, if you provided an API key earlier. Wavenet can be toggled here. Wavenet pitch modifies the voice pitch, while Wavenet speed modifies the speed accordingly. Next, wavenet voice allows you to choose the specific voice profile to use, while wavenet backup voice allows you to choose a second, lower cost, voice to use in radio downtime. That's it for wavenet options. After that, waitforuser allows this program to wait until you press enter before starting the radio. The next few options control how often a radio event occurs. For each of the following items, you can assign an arbitrary number. The higher the value, the less likely an item will play. Default PSA Chance refers to how often a public service announcement plays. Default Weather Chance refers to how often a weather report will be given. Default Welcome Chance refers to how often the radio intro will replay. Default Weekday Chance refers to how often the current playlist title will be mentioned. Finally, Default Time Chance refers to how often the current time will be mentioned. We're nearly done! Only a few more options. Next, scrolling limit is a useful option to force the web scraping engine to scroll down and gather more videos in a playlist. Set the number according to approximately how many times you need to scroll down in a playlist to see every thumbnail. For example, if there's 400 videos in a playlist on average, set this option to 4. Next, city name refers to the city name for OpenWeatherMap weather info. After that, override playlist allows you to set one single playlist to play all the time on the radio. Writeoutput and Write song info are deprecated options to write the current announcer voice lines and song info to a text file for use in programs like OBS Studio if livestreaming. Finally, PSA playlist URL allows you to set a YouTube playlist full of public service announcements to play on the air. Once you have a chance to modify each value to your liking, press enter to continue.")
        try:
            dummyvalue = input("Press enter to continue.")
        except (EOFError):
            pass
        speak("Thanks for taking the time to set up this software with the guided tutorial! If you wish to get more creative, check out some of the other files in the main directory here. You can even modify how the announcer reads weather info, have multiple stations with different configurations run at the same time, or adjust the layout of the website on this program's web server. When you are ready to begin the radio, press enter.")
        try:
            dummyvalue = input("Press enter to continue.")
        except (EOFError):
            pass
        os.execv(sys.executable, ['python3'] + sys.argv) # Restart the script by issuing a terminal command

    def startradio(self, customlocation="", loopforever=True):
        # Set URL, weekday text, etc. Plus, download playlists
        try:
            playlistmodule = __import__("PlaylistSearch" + str(customlocation))
        except (ImportError, FileNotFoundError):
            playlistmodule = __import__("PlaylistSearch")
            pass

        # Setup AI text generation
        # textgen = textgenrnn()
        # drawUI("[INFO] Test phrase: " + str(textgen.generate())) # Debug, print random AI-generated sentence to stdout

        # Init TTS engine
        engine = pyttsx3.init()
        # engine.setProperty('rate', 185) # Set speech rate
        engine.setProperty('volume',1.0) # Set speech volume

        # Init random number generation
        random.seed(a=None, version=2) # Set random seed based on current time

        # Init audio engine with 10 channels
        mixer = pygame.mixer
        mixer.pre_init(44100, -16, 2, 64)
        mixer.init()
        mixer.set_num_channels(8)
        pygame.init()

        # Determine main program directory
        maindirectory = os.path.dirname(os.path.abspath(__file__)) # The absolute path to this file

        # Retrieve options from JSON file
        try:
            with open(str(maindirectory) + '/Options' + str(customlocation) + '.json', 'r') as json_file:
                options_dict = json.load(json_file)

            # Read options from JSON file
            playintro = options_dict["playintro"] # Play the radio show intro on launch
            receivesuggestions = options_dict["suggestions"] # Bool for whether or not to incorporate song suggestions from the audience
            normalize_bool = options_dict["normalize_audio"] # Bool for whether or not to normalize each song with PyDub
            webport = options_dict["port"] # The port number for the webserver
            usedashboard = options_dict["dashboard"] # Bool for whether or not to use custom terminal layout
            offlinemode = options_dict["offline_mode"] # Bool to prevent making API calls of any kind
            maxsonglength = options_dict["max_song_length"]
            wavenet = options_dict["wavenet"] # Bool for whether or not to use Google TTS API
            wavenetpitch = options_dict["wavenet_pitch"] # (Double) pitch value for wavenet voice
            wavenetspeed = options_dict["wavenet_speed"] # (Double) speed value for wavenet voice
            wavenetvoice = options_dict["wavenet_voice"] # (String) wavenet voice profile [EX: "en-US-Wavenet-I"]
            wavenetbackupvoice = options_dict["wavenet_backup_voice"] # (String) wavenet backup voice profile [EX: "en-US-Standard-I"]
            waitforuser = options_dict["waitforuser"] # Bool for whether or not to wait for user input before starting radio
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
        except FileNotFoundError:
            print("[WARN] \"Options.json\" file cannot be found. Please redownload the file from Github. Script cannot continue.")
            quit()

        # Declare System Variables
        longspeechstring = "" # Used to append multiple strings before synthesizing audio
        playpsa = False # Bool value for whether or not a PSA will play immediately following a song
        listPlayedSongs = [] # List stores all song numbers that have already been played
        potentialsong = 1 # The index of the song to be played
        songsuggestion = False # Whether or not a suggested song if about to play
        psachance = defaultpsachance # Likelihood of playing a PSA [1/[x] chance]
        weatherchance = defaultweatherchance # Likelihood of mentioning the weather [1/[x] chance]
        welcomechance = defaultwelcomechance # Likelihood of mentioning the welcome message again [1/[x] chance]
        weekdaychance = defaultweekdaychance # Likelihood of mentioning the weekday again [1/[x] chance]
        timechance = defaulttimechance # Likelihood of mentioning the time [1/[x] chance]
        savedtime = "" # The text version of the time. Used to compare to actual time and determine when to start the next playlist

        # Init console dashboard
        masterdashboard = Dashboard("Automated Radio Station")

        # Custom function to draw to the dashboard's log
        def drawUI(text):
            if usedashboard:
                masterdashboard.UpdateUI(str(text).replace("\n"," "), round((1/psachance)*100), round((1/weatherchance)*100), round((1/welcomechance)*100), round((1/weekdaychance)*100), round((1/timechance)*100))
            else:
                print(text)

        # Check for errors
        # [Song Length]
        if maxsonglength < 0:
            raise NegativeMaximumSongLength
        
        # [City Name as Int]
        if not isinstance(city_name, str):
            raise TypeError

        # [Playlist Domain {Override}]
        if overrideplaylist.lower().find("youtube") != -1 and overrideplaylist.lower().find("youtu.be") != -1:
            raise PlaylistDomainError
        
        # [Playlist Domain {PSA}]
        if psaplaylisturl.lower().find("youtube") != -1 and psaplaylisturl.lower().find("youtu.be") != -1:
            raise PlaylistDomainError

        # [Random Bounds]
        if defaultpsachance < 0:
            raise NegativeRandomBounds
        elif defaultweatherchance < 0:
            raise NegativeRandomBounds
        elif defaultwelcomechance < 0:
            raise NegativeRandomBounds
        elif defaultweekdaychance < 0:
            raise NegativeRandomBounds
        elif defaulttimechance < 0:
            raise NegativeRandomBounds


        # If online, init web server
        if not offlinemode:
            # Init WebServer through subprocess, if port is selected in Options.json
            if isinstance(webport, int):
                if webport >= 0:
                    subprocess.Popen(["python3", str(maindirectory) + "/WebServer.py", str(webport), str(customlocation)])
                else:
                    raise NegativePortNumber
            else:
                drawUI("[INFO] A port for WebServer has not been set. WebServer is disabled.")

        # Override radio intro if specified by script args
        if len(sys.argv) > 1:
            if "skipintro" in sys.argv:
                playintro = False
                drawUI("[INFO] Script arguments specified playintro to False! Skipping radio intro sequence.")

        # Retrieve API keys from JSON file
        try:
            with open(str(maindirectory) + '/APIKeys.json', 'r') as json_file:
                APIkeys_dict = json.load(json_file)
            weatherkey = str(APIkeys_dict["Openweathermap"]) # API key for Openweathermap
        except FileNotFoundError:
            drawUI("[WARN] \"APIKeys.json\" could not be found. Continuing without API keys ...")
            pass

        # Return list of sound filenames, only with extensions .ogg and .wav
        directory= os.path.join(maindirectory,"Assets/SoundEffects" + str(customlocation))
        try:
            radiosound_dict = [x for x in os.listdir(directory) if ".wav" or ".WAV" or ".Wav" or ".ogg" or ".OGG" or ".Ogg" in x]
            for item in radiosound_dict:
                if item.upper().count(".WAV") == 0 and item.upper().count(".OGG") == 0:
                    radiosound_dict.remove(item)
            radiosoundcount = len(radiosound_dict) - 1
            if radiosoundcount < 0:
                radiosoundcount = 0
        except FileNotFoundError:
            radiosound_dict = []
            radiosoundcount = 0

        # Return list of music filenames, only with extensions .ogg and .wav
        directory= os.path.join(maindirectory,"DownloadedSongs" + str(customlocation))
        try:
            radiomusic_dict = [x for x in os.listdir(directory) if ".wav" or ".WAV" or ".Wav" or ".ogg" or ".OGG" or ".Ogg" in x]
            for item in radiomusic_dict:
                if item.upper().count(".WAV") == 0 and item.upper().count(".OGG") == 0:
                    radiomusic_dict.remove(item)
            radiomusiccount = len(radiomusic_dict) - 1
            if radiomusiccount < 0:
                radiomusiccount = 0
        except FileNotFoundError:
            radiomusic_dict = []
            radiomusiccount = 0

        # Custom function to dump some statistics to a JSON file, which is picked up by the Web Server
        def variable_dump():
            data = {}
            data["Statistics"] = []
            if not songsuggestion:
                data["Statistics"].append({"PlaylistURL": str(musicplaylist), "SongsPlayedNum": len(listPlayedSongs),"SongTitle": str(playlistnames[songselectionint]),"EmbedLink": videoID.replace("https://www.youtube.com/watch?v=","https://www.youtube.com/embed/"),"SongLink": videoID, "WeatherDecimal": round((1/weatherchance)*100), "PSADecimal": round((1/psachance)*100), "WelcomeDecimal": round((1/welcomechance)*100), "WeekdayDecimal": round((1/weekdaychance)*100), "TimeDecimal": round((1/timechance)*100)})
            else:
                data["Statistics"].append({"PlaylistURL": str(musicplaylist), "SongsPlayedNum": len(listPlayedSongs),"SongTitle": "Audience Suggestion","EmbedLink": videoID.replace("https://www.youtube.com/watch?v=","https://www.youtube.com/embed/").replace("https://youtu.be/","https://www.youtube.com/embed/"),"SongLink": videoID, "WeatherDecimal": round((1/weatherchance)*100), "PSADecimal": round((1/psachance)*100), "WelcomeDecimal": round((1/welcomechance)*100), "WeekdayDecimal": round((1/weekdaychance)*100), "TimeDecimal": round((1/timechance)*100)})
            with open(str(maindirectory) + "/VariableDump" + str(customlocation) + ".json", "w") as jsonfile:
                json.dump(data, jsonfile)

        # Custom function to retrieve video suggestion links
        def parse_suggestions():
            try:
                with open(str(maindirectory) + "/SuggestionDump" + str(customlocation) + ".json", "r") as json_file:
                    suggestion_dict_parent = json.load(json_file)
                    suggestion_dict = suggestion_dict_parent["Suggestion"][0]
                    json_file.close()
                os.remove(str(maindirectory) + "/SuggestionDump" + str(customlocation) + ".json")
                newsuggestion = str(suggestion_dict["Link"])
                drawUI(f"[INFO] New suggestion found! {newsuggestion}")
                return newsuggestion
            except FileNotFoundError:
                drawUI("[INFO] No new suggestions yet.")
                return ""

        # Google Cloud TTS Function to Generate Wavenet Samples
        def text_to_wav(text, earlyfade = False):
            # If the current time is in the early morning, save money by switching to backup voice
            timeobject = datetime.now()
            currenttime = int(timeobject.strftime("%H"))
            if currenttime >= 0 and currenttime < 8:
                voice_name = wavenetbackupvoice
            else:
                voice_name = wavenetvoice

            language_code = "-".join(voice_name.split("-")[:2])
            text_input = texttospeech.SynthesisInput(text=text)
            voice_params = texttospeech.VoiceSelectionParams(
                language_code=language_code, name=voice_name
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                speaking_rate=wavenetspeed,
                pitch=wavenetpitch
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
            mixer.Channel(0).play(voice, fade_ms=50)
            if earlyfade: # If specified, continue running code 5 seconds before sound ends
                waittime = (voice.get_length()*1000) - 5000
                if waittime < 0:
                    waittime = voice.get_length()*1000
                # pygame.time.wait(waittime)
                time.sleep(waittime/1000)
            else:
                time.sleep(voice.get_length())

        # Custom function to just speak text with system TTS
        def speaktext(message, earlyfade=False):
            drawUI("[SPEECH] " + "\"" + str(message) + "\"") # Print the message contents to stdout
            # If enabled, write message contents to text file for use in OBS Studio
            if writeoutput:
                with open(str(maindirectory) + "/Output" + str(customlocation) + ".txt","w") as fileoutput:
                    fileoutput.write("\n" + str(message))
                    fileoutput.close()
            if wavenet and not offlinemode:
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
                    os.system("espeak \"" + str(message).replace("'","").replace("\"","") + "\"")

        # Tell user that the program is starting
        speaktext("We'll be right back!")

        # Start a random radio "waiting" song
        if radiomusiccount > 0:
            waitingsound = mixer.Sound(str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/" + str(radiomusic_dict[random.randint(0,radiomusiccount)]))
            waitingsound.set_volume(0.4)
            if not offlinemode: # If offline, no need to wait
                mixer.Channel(1).play(waitingsound, fade_ms=1000, loops=999)

        # State any errors/warnings to user
        if weatherkey == "":
            drawUI("[WARN] " + "You have not provided an Openweathermap API key. The API key is required to give weather info.")

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
        drawUI("[INFO] " + "The time is currently " + str(currenttime) + ".")

        # Set the following VARs according to the current time, for use in the IF statements below
        timeobject = datetime.now()
        currenttime = int(timeobject.strftime("%H"))

        # Set the appropriate playlist according to the weekday using custom PlaylistSearch function w/ classes
        playlistselection = playlistmodule.Playlist(datetime.today().weekday(), currenttime)
        url = playlistselection.get_URL()
        playlistID = url.replace("https://www.youtube.com/playlist?list=","")
        savedweekday = playlistselection.get_savedweekday()
        savedtime = playlistselection.get_savedtime()
        weekdaytext = playlistselection.get_weekdaytext()

        # If the playlist URL is still blank, warn the user and use a fallback playlist
        if url == "":
            url = "https://www.youtube.com/playlist?list=PLHL1i3oc4p0o76QOZ_BLZwjDb1x21azmC"
            drawUI("[WARN] " + "You didn't specify a music playlist for today's date! Using fallback playlist.")

        # If specified, override the weekday playlist with something else
        if overrideplaylist:
            url = overrideplaylist
            drawUI("[INFO] " + "Override enabled for playlist. Using " + str(url) + ".")

        # Declare lists for playlist video URLs, titles, and video IDs
        playlist=[]
        playlistnames=[]
        playlistIDs=[]

        # If offline mode isn't set, do the following
        if not offlinemode:
            # Print steps to stdout
            drawUI("[INFO] " + "Downloading latest music playlist information from YouTube ...")

            # Set Firefox to run in headless mode
            opts = FirefoxOptions()
            opts.add_argument("--headless")
            driver = webdriver.Firefox(options=opts)

            # Open playlist URL in headless Firefox
            driver.get(url)
            playlisturl = url

            countervar = 1 # Used to display how many videos have been gathered

            # Continue to scroll down the playlist until most of playlist is in view
            scrollcounter = 0
            while scrollcounter < scrollinglimit:
                scrolldriver = driver.find_element_by_tag_name("html")
                scrolldriver.send_keys(Keys.END)
                time.sleep(2)
                scrollcounter += 1
                drawUI(f"[INFO] (Index {scrollcounter}) Scrolling to next page in playlist.")

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
                    name = longname_concat
                else:
                    name = longname_concat[:end]
                if name != "": # If title exists, add name and link to the lists
                    drawUI(f"[INFO] (Video Index {str(countervar)}) Retrieved info for \"{name}\"")
                    playlist.append(link)
                    playlistnames.append(name)
                    countervar += 1

            musicplaylist=vidstrip(playlist) # Strip unneccessary chars from list
            driver.close() # Close the web rendering engine

            # Clone URL list and remove everything except YouTube video IDs
            for item in playlist:
                playlistIDs.append(item.replace("https://www.youtube.com/watch?v=",""))

            # Print message to stdout
            drawUI("[INFO] " + "Finished downloading info from music playlist.")

            # Save Playlist URLs to Disk
            filePlaylist = open(str(maindirectory) + "/Cache-" + str(url.replace("https://www.youtube.com/playlist?list=","")) + "_URL.txt", "w")
            for item in musicplaylist:
                filePlaylist.write(item + "\n")
            filePlaylist.close()

            # Save Playlist Names to Disk
            filePlaylist = open(str(maindirectory) + "/Cache-" + str(url.replace("https://www.youtube.com/playlist?list=","")) + "_NAME.txt", "w")
            for item in playlistnames:
                filePlaylist.write(item + "\n")
            filePlaylist.close()

        else: # If offline, gather list from disk
            # Open current playlist URLs
            try:
                filePlaylist = open(str(maindirectory) + "/Cache-" + str(url.replace("https://www.youtube.com/playlist?list=","")) + "_URL.txt", "r")
                musicplaylist = filePlaylist.readlines()
                filePlaylist.close()
                iteration = 0
                while iteration < len(musicplaylist):
                    musicplaylist[iteration] = musicplaylist[iteration].replace("\n","")
                    iteration += 1
            except FileNotFoundError:
                speaktext("You are offline and I cannot find the playlist file on the disk. Please go online and try again.")
                quit()
            # Open current playlist names
            try:
                filePlaylist = open(str(maindirectory) + "/Cache-" + str(url.replace("https://www.youtube.com/playlist?list=","")) + "_NAME.txt", "r")
                playlistnames = filePlaylist.readlines()
                filePlaylist.close()
                iteration = 0
                while iteration < len(playlistnames):
                    playlistnames[iteration] = playlistnames[iteration].replace("\n","")
                    iteration += 1
            except FileNotFoundError:
                speaktext("You are offline and I cannot find the playlist file on the disk. Please go online and try again.")
                quit()
            # Clone URL list and remove everything except YouTube video IDs
            for item in musicplaylist:
                playlistIDs.append(item.replace("https://www.youtube.com/watch?v=",""))

        # Open SongArchive file to avoid excessive YouTube-DL calls
        try:
            fileSongArchive = open(str(maindirectory) + "/SongArchive" + str(customlocation) + ".txt", "r")
            songarchive = fileSongArchive.readlines()
            fileSongArchive.close()
        except FileNotFoundError:
            songarchive = []
            pass

        # If online and new files exist in playlist, save entire playlist to disk
        match = True # Set var to check if there's a new song
        for item in playlistIDs:
            checkitem = "youtube " + str(item) + "\n"
            if checkitem not in songarchive:
                match = False

        if match == False and not offlinemode:
            drawUI("[INFO] " + "Saving music playlist to disk ...")
            speaktext("We have a few new songs here. We'll be back after I add them to the mix.")
            ydl_opts = {"outtmpl": str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/%(id)s.%(ext)s", "ignoreerrors": True, "format": "bestaudio[ext=m4a]", "geobypass": True, "noplaylist": True, "source_address": "0.0.0.0", "download_archive": str(maindirectory) + "/SongArchive" + str(customlocation) + ".txt", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "vorbis"}]}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                videocounter = 0
                videolist = []
                while videocounter < len(musicplaylist):
                    videolist.clear()
                    videolist.append(str(musicplaylist[videocounter]))
                    checkstring = "youtube " + str(musicplaylist[videocounter]).replace("https://www.youtube.com/watch?v=","") + "\n"
                    if checkstring not in songarchive:
                        ydl.download(videolist)
                        try:
                            if normalize_bool:
                                beforesound = AudioSegment.from_file(str(str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/" + str(musicplaylist[videocounter]) + ".ogg").replace("https://www.youtube.com/watch?v=",""), "ogg")  
                                aftersound = effects.normalize(beforesound)  
                                aftersound.export(str(str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/" + str(musicplaylist[videocounter]) + ".ogg").replace("https://www.youtube.com/watch?v=",""), format="ogg", tags={"title": "AutomatedRadioStation"})
                                beforesound.close()
                                aftersound.close()
                                del beforesound
                                del aftersound
                                gc.collect() # Free memory
                            drawUI(f"[INFO] Downloaded ({videocounter + 1}/{len(musicplaylist)}).")
                        except FileNotFoundError:
                            drawUI(f"[INFO] Failed to download ({videocounter + 1}/{len(musicplaylist)}).")
                            pass
                    videocounter += 1

        # Open PSAArchive file to avoid excessive YouTube-DL calls
        try:
            filePSAArchive = open(str(maindirectory) + "/PSAArchive" + str(customlocation) + ".txt", "r")
            PSAArchive = filePSAArchive.readlines()
            filePSAArchive.close()
        except FileNotFoundError:
            PSAArchive = []
            pass

        # Declare appropriate "playlist" lists
        playlist=[] # Clear "playlist" list
        playlistnamesPSA=[]
        playlistIDsPSA=[]

        # If offline mode isn't set, scrape the PSA playlist (if playlist URL is specified)
        if not offlinemode:
            if psaplaylisturl != "":
                # Set URL for PSAs instead of music
                url = psaplaylisturl

                # Print steps to stdout
                drawUI("[INFO] " + "Downloading latest PSA playlist information from YouTube ...")

                # Run Firefox in automated headless mode
                opts = FirefoxOptions()
                opts.add_argument("--headless")
                driver = webdriver.Firefox(options=opts)
                driver.get(url) # Open URL
                countervar = 1 # Used to display how many videos have been gathered

                # Continue to scroll down the playlist until most of playlist is in view
                scrollcounter = 0
                while scrollcounter < scrollinglimit:
                    scrolldriver = driver.find_element_by_tag_name("html")
                    scrolldriver.send_keys(Keys.END)
                    time.sleep(2)
                    scrollcounter += 1
                    drawUI(f"[INFO] (Index {scrollcounter}) Scrolling to next page in playlist.")

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
                        name = longname_concat
                    else:
                        name = longname_concat[:end]
                    if name != "": # If title exists, add name and link to the lists
                        playlist.append(link2) # Append each URL to the list
                        playlistnamesPSA.append(longname2)
                        drawUI(f"[INFO] (Video Index {str(countervar)}) Retrieved info for \"{longname2}\"")
                        countervar += 1

                psaplaylist=vidstrip(playlist)
                driver.close() # Close the web rendering engine

                # Clone URL list and remove everything except YouTube video IDs
                for item in playlist:
                    playlistIDsPSA.append(item.replace("https://www.youtube.com/watch?v=",""))
                
                # Save Playlist URLs to Disk
                filePlaylist = open(str(maindirectory) + "/Cache-" + str(psaplaylisturl.replace("https://www.youtube.com/playlist?list=","")) + "_URL.txt", "w")
                for item in psaplaylist:
                    filePlaylist.write(item + "\n")
                filePlaylist.close()
            else:
                # Print missing playlist info message to stdout
                drawUI("[INFO] " + "PSA playlist URL has not been set. The station will not play PSAs.")
        
        if offlinemode and psaplaylisturl != "": # If offline, gather list from disk
            # Open current playlist URLs
            try:
                filePlaylist = open(str(maindirectory) + "/Cache-" + str(psaplaylisturl.replace("https://www.youtube.com/playlist?list=","")) + "_URL.txt", "r")
                psaplaylist = filePlaylist.readlines()
                filePlaylist.close()
                iteration = 0
                while iteration < len(psaplaylist):
                    psaplaylist[iteration] = psaplaylist[iteration].replace("\n","")
                    iteration += 1
            except FileNotFoundError:
                speaktext("You are offline and I cannot find the playlist file on the disk. Please go online and try again.")
                quit()
            # Clone URL list and remove everything except YouTube video IDs
            for item in psaplaylist:
                playlistIDs.append(item.replace("https://www.youtube.com/watch?v=",""))

        # If online and new files exist in playlist, save entire playlist to disk
        match = True # Set var to check if there's a new song
        for item in playlistIDsPSA:
            checkitem = "youtube " + str(item) + "\n"
            if checkitem not in PSAArchive:
                match = False

        if match == False and not offlinemode:
            drawUI("[INFO] " + "Saving PSA playlist to disk ...")
            speaktext("Almost there, we have a few PSAs to add to the show.")
            ydl_opts = {"outtmpl": str(maindirectory) + "/DownloadedPSAs" + str(customlocation) + "/%(id)s.%(ext)s", "ignoreerrors": True, "format": "bestaudio[ext=m4a]", "geobypass": True, "noplaylist": True, "source_address": "0.0.0.0", "download_archive": str(maindirectory) + "/PSAArchive" + str(customlocation) + ".txt", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "vorbis"}]}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                videocounter = 0
                videolist = []
                while videocounter < len(psaplaylist):
                    videolist.clear()
                    videolist.append(str(psaplaylist[videocounter]))
                    checkstring = "youtube " + str(psaplaylist[videocounter]).replace("https://www.youtube.com/watch?v=","") + "\n"
                    if checkstring not in PSAArchive:
                        ydl.download(videolist)
                        try:
                            if normalize_bool:
                                beforesound = AudioSegment.from_file(str(str(maindirectory) + "/DownloadedPSAs" + str(customlocation) + "/" + str(psaplaylist[videocounter]) + ".ogg").replace("https://www.youtube.com/watch?v=",""), "ogg")  
                                aftersound = effects.normalize(beforesound)  
                                aftersound.export(str(str(maindirectory) + "/DownloadedPSAs" + str(customlocation) + "/" + str(psaplaylist[videocounter]) + ".ogg").replace("https://www.youtube.com/watch?v=",""), format="ogg", tags={"title": "AutomatedRadioStation"})
                                beforesound.close()
                                aftersound.close()
                                del beforesound
                                del aftersound
                                gc.collect() # Free memory
                            drawUI(f"[INFO] Downloaded ({videocounter + 1}/{len(psaplaylist)}).")
                        except FileNotFoundError:
                            drawUI(f"[INFO] Failed to download ({videocounter + 1}/{len(psaplaylist)}).")
                            pass
                    videocounter += 1

            # Print completion message to stdout
            drawUI("[INFO] " + "Finished downloading info from PSA playlist. Starting radio ...")

        # Read and store each external speech script into memory
        # (Each line in the textfile represents a different index in the list)
        # This is used for text variation to make the announcer seem more lifelike.

        # Intro Text Short (Single sentence to welcome the listener)
        try:
            fileIntroTextShort = open(str(maindirectory) + "/SpeechScripts" + str(customlocation) + "/IntroTextShort.txt", "r")
            speechIntroTextShort = fileIntroTextShort.readlines()
            fileIntroTextShort.close()
        except FileNotFoundError:
            drawUI("[WARN] \"IntroTextShort.txt\" cannot be found. Try redownloading the program? Continuing anyway ...")
            speechIntroTextShort = "You are listening to PhysCorp's Automated Radio Station."
            pass

        # First Run Prompts (Describes the radio station in-detail)
        try:
            fileFirstrunPrompts = open(str(maindirectory) + "/SpeechScripts" + str(customlocation) + "/FirstrunPrompts.txt", "r")
            speechFirstrunPrompts = fileFirstrunPrompts.readlines()
            fileFirstrunPrompts.close()
        except FileNotFoundError:
            drawUI("[WARN] \"FirstrunPrompts.txt\" cannot be found. Try redownloading the program? Continuing anyway ...")
            speechFirstrunPrompts = "Welcome to the fully automated radio station."
            pass

        # Song Transitions (Variations on describing which song comes next)
        try:
            fileSongTransitions = open(str(maindirectory) + "/SpeechScripts" + str(customlocation) + "/SongTransitions.txt", "r")
            speechSongTransitions = fileSongTransitions.readlines()
            fileSongTransitions.close()
        except FileNotFoundError:
            drawUI("[WARN] \"SongTransitions.txt\" cannot be found. Try redownloading the program? Continuing anyway ...")
            speechFirstrunPrompts = "Up next is "
            pass

        # Song END Transitions (Variations on what song you just heard)
        try:
            fileSongEndTransitions = open(str(maindirectory) + "/SpeechScripts" + str(customlocation) + "/SongEndTransitions.txt", "r")
            speechSongEndTransitions = fileSongEndTransitions.readlines()
            fileSongEndTransitions.close()
        except FileNotFoundError:
            drawUI("[WARN] \"SongEndTransitions.txt\" cannot be found. Try redownloading the program? Continuing anyway ...")
            speechFirstrunPrompts = "You just heard "
            pass

        # Prepare the intro lines with synthesized voice
        longspeechstring = "" # Clear the longspeechstring var

        # If the playlist isn't overridden, add the weekday text to longspeechstring var
        if not overrideplaylist:
            longspeechstring += str(weekdaytext)

        # Add a random variation of the "Intro Text Short" speech to longspeechstring var & include the version number
        longspeechstring += " " + str(speechIntroTextShort[random.randint(0,len(speechIntroTextShort)-1)])
        # longspeechstring += " Version " + str(VERSION_INFO) + "."

        # Add a random variation of the "First Run Prompts" speech to longspeechstring var
        longspeechstring += " " + str(speechFirstrunPrompts[random.randint(0,len(speechFirstrunPrompts)-1)])

        # Stop the waiting sound, fading out for 1 second
        if radiomusiccount > 0:
            waitingsound.fadeout(1000)

        # Wait for the user to press ENTER if they specified waiting in Options.json
        if waitforuser:
            drawUI("[INFO] The radio is ready! Press ENTER to start.")
            testinput = input("")

        # Loop through songs, announcements, and other commentary forever
        while loopforever:
            try: # Uses "try except" loop, ensuring that if an error occurs, the script will restart automatically
                # Set the random seed again based on current time
                random.seed(a=None, version=2)
                
                # Play radio intro if enabled
                if playintro == True:
                    # Play random radio sound before speaking (if file exists)
                    if radiosoundcount >= 1:
                        sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects" + str(customlocation) + "/" + str(radiosound_dict[random.randint(0,radiosoundcount)]))
                        sound.set_volume(0.3)
                        mixer.Channel(2).play(sound, fade_ms=50)
                        waittime = (sound.get_length()*1000)/2
                        if waittime < 0:
                            waittime = sound.get_length()*1000
                        # pygame.time.wait(waittime)
                        time.sleep(waittime/1000)
                    
                    # Play the background waiting sound while the announcer speaks
                    if radiomusiccount > 0:
                        newwaitingsound = mixer.Sound(str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/" + str(radiomusic_dict[random.randint(0,radiomusiccount)]))
                        newwaitingsound.set_volume(0.1)
                        mixer.Channel(3).play(newwaitingsound, fade_ms=1000)

                    # Play the synthesized voice
                    speaktext(longspeechstring)

                    # Stop the waiting sound, fading out for 1 second
                    if radiomusiccount > 0:
                        newwaitingsound.fadeout(1000)

                    # Play random radio sound after speaking (if file exists)
                    if radiosoundcount >= 1:
                        sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects" + str(customlocation) + "/" + str(radiosound_dict[random.randint(0,radiosoundcount)]))
                        sound.set_volume(0.3)
                        mixer.Channel(2).play(sound, fade_ms=50)
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
                    drawUI("[INFO] " + "List of completed song indexes:\n\t" + str(listPlayedSongs)) # Show list of played song numbers
                    drawUI("[INFO] " + "Likelihood VARs:\n\tPSA: [1/" + str(psachance) + "]\tWeather: [1/" + str(weatherchance) + "]\tWelcomeMessage: [1/" + str(welcomechance) + "]\tWeekdayMessage: [1/" + str(weekdaychance) + "]\tTime: [1/" + str(timechance) + "]") # Show chance VARs

                    longspeechstring = "" # Clear the longspeechstring var
                    longspeechstring += " " + str(speechSongTransitions[random.randint(0,len(speechSongTransitions)-1)]) + str(playlistnames[songselectionint]) + "."
                    # longspeechstring += " " + str(speechSongTransitions[random.randint(0,len(speechSongTransitions)-1)]) + str(playlistnames[songselectionint]) + "."
                    
                    # Chance to speak "Stay safe!"
                    if random.randint(0,4) == 1:
                        longspeechstring += " Stay safe!"
                    
                    # Use system TTS engine to speak the next song info
                    speaktext(longspeechstring, earlyfade=True)

                    # Play random radio sound after speaking (if file exists)
                    if radiosoundcount >= 1:
                        sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects" + str(customlocation) + "/" + str(radiosound_dict[random.randint(0,radiosoundcount)]))
                        sound.set_volume(0.3)
                        mixer.Channel(2).play(sound, fade_ms=50)
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

                suggestioninfo = [{"title": ""}]
                newsong = False
                if not songsuggestion:
                    videoID = str(musicplaylist[songselectionint])
                else:
                    videoID = potentialsuggestion
                    if videoID.find("youtube.com/watch?v=") == -1 and videoID.find("youtu.be/") == -1:
                        # Link is NOT valid
                        drawUI("[INFO] The suggested song is not a valid YouTube link.")
                        speaktext("Never mind. It looks like the suggested link is not valid. I'm resuming normal playback.")
                        newsong = True
                    else:
                        # Link is valid
                        shortvideoID = potentialsuggestion.replace("https://www.youtube.com/watch?v=","").replace("https://youtu.be/","")
                        # end=shortvideoID.find("&")
                        # videoID = str(shortvideoID[:end+1])

                        # Download the next song info with YouTube-DL
                        ydl_opts = {"outtmpl": str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/%(id)s.%(ext)s", "ignoreerrors": True, "format": "bestaudio[ext=m4a]", "geobypass": True, "source_address": "0.0.0.0", "noplaylist": True, "download_archive": str(maindirectory) + "/SongArchive" + str(customlocation) + ".txt", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "vorbis"}]}
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            suggestioninfo = ydl.extract_info(videoID, download=False)
                        
                        # If the video has an age limit, skip it and find a new song
                        if suggestioninfo["age_limit"] > 0:
                            drawUI("[INFO] The suggested song has an age limit.")
                            speaktext("Never mind. It looks like the suggested song has an age limit and is not suitable for the radio. I'm resuming normal playback.")
                            newsong = True
                        else:
                            drawUI("[INFO] Song is NOT age restricted. Continuing playback.")

                # If the suggestion cannot be played, or is flagged for another reason, choose a new song
                if newsong:
                    # Randomly choose a new song from the playlist
                    if len(listPlayedSongs) >= len(musicplaylist) - 1: # If the music list has been exhausted
                        listPlayedSongs.clear() # Clear the list and start again
                    while potentialsong in listPlayedSongs: # If the song has been chosen already,
                        potentialsong = random.randint(1,len(musicplaylist)-1) # Randomly select a new song from the playlist
                    listPlayedSongs.append(potentialsong) # Add the song index to the list of played songs
                    songselectionint = potentialsong # Set the next song to the one that was randomly chosen
                    videoID = str(musicplaylist[songselectionint])
                    newsong = False

                # Reset songsuggestion var
                songsuggestion = False

                # If the file has not been downloaded, do the following
                if not os.path.exists(str(str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/" + videoID + ".ogg").replace("https://www.youtube.com/watch?v=","")) and not offlinemode:
                    # Download the next song as a OGG file with YouTube-DL
                    ydl_opts = {"outtmpl": str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/%(id)s.%(ext)s", "ignoreerrors": True, "format": "bestaudio[ext=m4a]", "geobypass": True, "source_address": "0.0.0.0", "noplaylist": True, "download_archive": str(maindirectory) + "/SongArchive" + str(customlocation) + ".txt", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "vorbis"}]}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        # ydl.download(videoID)
                        info = ydl.extract_info(videoID, download=True)
                    # Normalize the audio
                    if normalize_bool:
                        drawUI("[INFO] Normalizing audio ...")
                        beforesound = AudioSegment.from_file(str(str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/" + videoID + ".ogg").replace("https://www.youtube.com/watch?v=",""), "ogg")  
                        aftersound = effects.normalize(beforesound)  
                        aftersound.export(str(str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/" + videoID + ".ogg").replace("https://www.youtube.com/watch?v=",""), format="ogg", tags={"title": "AutomatedRadioStation"})
                        beforesound.close()
                        aftersound.close()
                        del beforesound
                        del aftersound
                        gc.collect() # Free memory

                # Play the downloaded song with pygame mixer
                try:
                    music = mixer.Sound(str(str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/" + videoID + ".ogg").replace("https://www.youtube.com/watch?v=",""))
                    music.set_volume(0.7)
                    mixer.Channel(4).play(music, fade_ms=5000)
                    waittime = (music.get_length()*1000) - 5000
                    if waittime < 0:
                        waittime = music.get_length()*1000
                    if waittime > maxsonglength*60000: # If song is greater than specified max length in ms
                        waittime = maxsonglength*60000 # Set song length to specified max length in ms
                        longspeechstring += "That's enough of that song. "
                    # pygame.time.wait(waittime)
                    # Show operator that song is playing in stdout
                    drawUI("[INFO] " + "Currently playing " + str(playlistnames[songselectionint]) + ".")
                    drawUI("[DEBUG - SONG PATH] " + str(str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/" + videoID + ".ogg").replace("https://www.youtube.com/watch?v=",""))
                    variable_dump() # Dump variables to JSON file for use in WebServer
                    time.sleep(waittime/1000)
                    music.fadeout(4000)
                    # Song that just played
                    longspeechstring += str(speechSongEndTransitions[random.randint(0,len(speechSongEndTransitions)-1)]) + str(playlistnames[songselectionint]) + "."
                except (RuntimeError, TypeError, NameError, OSError, KeyError, IndexError, LookupError, FileNotFoundError):
                    speaktext("It looks like that song isn't available.")
                    pass

                # Listening to PhysCorp's Automated Station & Version Info
                longspeechstring += " " + str(speechIntroTextShort[random.randint(0,len(speechIntroTextShort)-1)])
                # longspeechstring += " Version " + str(VERSION_INFO) + "."

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
                if random.randint(0,weatherchance) == 1 and weatherkey != "" and welcomechance != defaultwelcomechance-1 and not offlinemode:
                    # Reset weatherchance var
                    weatherchance = defaultweatherchance
                    api_key = weatherkey
                    base_url = "http://api.openweathermap.org/data/2.5/weather?"

                    # Set city name [REFERENCED IN MAIN.PY OPTIONS]
                    # If blank, set city to Auburn Hills and print info to stdout
                    if city_name == "":
                        city_name = "Auburn Hills"
                        drawUI("[INFO] " + "A city name has not been set. Using Auburn Hills.")

                    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
                    response = requests.get(complete_url) 

                    x = response.json() 
                    if x["cod"] != "404": 
                        y = x["main"] 
                        current_temperature = (y["temp"])*1.8 - 459.67
                        current_humidity = y["humidity"] 
                        z = x["weather"] 
                        weather_description = z[0]["description"] 

                        # Include weather info in longspeechstring var
                        longspeechstring += " Let's check up on the weather outside! Here in " + str(city_name) + ", " 
                        weatherobject = WeatherSpeech(str(weather_description))
                        longspeechstring += weatherobject.returnspeech() + ". "
                        longspeechstring += "The temperature is currently " + str(round(current_temperature)) + " degrees."


                # Increase the chance to speak the weather info
                if weatherchance > 2:
                    weatherchance -= 1
                
                potentialsuggestion = parse_suggestions()
                if potentialsuggestion != "" and receivesuggestions:
                    songsuggestion = True
                else:
                    songsuggestion = False

                # If there isn't a new song suggestion, choose a song from the playlist
                if not songsuggestion:
                    # Randomly choose a new song from the playlist
                    if len(listPlayedSongs) >= len(musicplaylist) - 1: # If the music list has been exhausted
                        listPlayedSongs.clear() # Clear the list and start again
                    while potentialsong in listPlayedSongs: # If the song has been chosen already,
                        potentialsong = random.randint(1,len(musicplaylist)-1) # Randomly select a new song from the playlist
                    listPlayedSongs.append(potentialsong) # Add the song index to the list of played songs
                    songselectionint = potentialsong # Set the next song to the one that was randomly chosen
                    drawUI("[INFO] " + "List of completed song indexes:\n\t" + str(listPlayedSongs)) # Show list of played song numbers
                    drawUI("[INFO] " + "Likelihood VARs:\n\tPSA: [1/" + str(psachance) + "]\tWeather: [1/" + str(weatherchance) + "]\tWelcomeMessage: [1/" + str(welcomechance) + "]\tWeekdayMessage: [1/" + str(weekdaychance) + "]\tTime: [1/" + str(timechance) + "]") # Show chance VARs

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
                if not songsuggestion:
                    longspeechstring += " " + str(speechSongTransitions[random.randint(0,len(speechSongTransitions)-1)]) + str(playlistnames[songselectionint]) + "."
                else:
                    # Select the suggested song for playback, and include a disclaimer
                    longspeechstring += " It looks like there's a new song suggestion from one of our listeners. Just a disclaimer, I don't monitor the content of these videos. That being said, let's listen."

                # Chance to play a PSA
                if random.randint(0,psachance) == 1 and psaplaylisturl != "":
                    playpsa = True
                    longspeechstring += " But first, here's a brief message. Don't touch that dial."
                    # Reset psachance var
                    psachance = defaultpsachance

                # Chance to include "Stay safe!" in speech
                if random.randint(0,4) == 1:
                    longspeechstring += " Stay safe!"

                # Play random radio sound before speaking if file exists
                if radiosoundcount >= 1:
                    sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects" + str(customlocation) + "/" + str(radiosound_dict[random.randint(0,radiosoundcount)]))
                    sound.set_volume(0.3)
                    mixer.Channel(2).play(sound, fade_ms=50)
                    waittime = (sound.get_length()*1000)/2
                    if waittime < 0:
                        waittime = sound.get_length()*1000
                    # pygame.time.wait(waittime)
                    time.sleep(waittime/1000)
                
                # Play the background waiting sound while the announcer speaks
                if radiomusiccount > 0:
                    newwaitingsoundtwo = mixer.Sound(str(maindirectory) + "/DownloadedSongs" + str(customlocation) + "/" + str(radiomusic_dict[random.randint(0,radiomusiccount)]))
                    newwaitingsoundtwo.set_volume(0.1)
                    mixer.Channel(5).play(newwaitingsoundtwo, fade_ms=1000)

                # If the time is midnight (if stored weekday info doesn't match current weekday info), restart the script to gather new playlist info
                if savedweekday != datetime.today().weekday() and overrideplaylist == "":
                    speaktext("We're ready for a new playlist. Coming up in a sec!")
                    if radiomusiccount > 0:
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
                if savedtimecomparison != savedtime and overrideplaylist == "":
                    speaktext("We're ready for a new playlist. Coming up in a sec!")
                    waitingsound.stop()
                    os.execv(sys.executable, ['python3'] + sys.argv) # Restart the script by issuing a terminal command

                # Play the synthesized speech
                speaktext(longspeechstring)

                # Stop the waiting sound, fading out for 1 second
                if radiomusiccount > 0:
                    newwaitingsoundtwo.fadeout(1000)

                # Play the PSA if triggered
                if playpsa == True:
                    playpsa = False # Prevent PSA from running twice
                    
                    # Play the PSA, if the video isn't available, repeat the process until one is
                    while True:
                        try:
                            playlistitem = str(psaplaylist[random.randint(1,len(psaplaylist)-1)])
                            if not os.path.exists(str(str(maindirectory) + "/DownloadedPSAs" + str(customlocation) + "/" + playlistitem + ".ogg").replace("https://www.youtube.com/watch?v=","")) and not offlinemode:
                                # Download the next song as a OGG file with YouTube-DL
                                ydl_opts = {"outtmpl": str(maindirectory) + "/DownloadedPSAs" + str(customlocation) + "/%(id)s.%(ext)s", "ignoreerrors": True, "format": "bestaudio[ext=m4a]", "geobypass": True, "source_address": "0.0.0.0", "noplaylist": True, "download_archive": str(maindirectory) + "/PSAArchive" + str(customlocation) + ".txt", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "vorbis"}]}
                                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                    # ydl.download(videoID)
                                    info = ydl.extract_info(playlistitem, download=True)
                                # Normalize the audio
                                if normalize_bool:
                                    drawUI("[INFO] Normalizing audio ...")
                                    beforesound = AudioSegment.from_file(str(str(maindirectory) + "/DownloadedPSAs" + str(customlocation) + "/" + playlistitem + ".ogg").replace("https://www.youtube.com/watch?v=",""), "ogg")  
                                    aftersound = effects.normalize(beforesound)  
                                    aftersound.export(str(str(maindirectory) + "/DownloadedPSAs" + str(customlocation) + "/" + playlistitem + ".ogg").replace("https://www.youtube.com/watch?v=",""), format="ogg", tags={"title": "AutomatedRadioStation"})
                                    beforesound.close()
                                    aftersound.close()
                                    del beforesound
                                    del aftersound
                                    gc.collect() # Free memory

                            # Play the downloaded song with pygame mixer
                            psa = mixer.Sound(str(str(maindirectory) + "/DownloadedPSAs" + str(customlocation) + "/" + playlistitem + ".ogg").replace("https://www.youtube.com/watch?v=",""))
                            psa.set_volume(0.7)
                            mixer.Channel(6).play(psa, fade_ms=1000)
                            waittime = psa.get_length()*1000
                            # pygame.time.wait(waittime)
                            # Show operator that song is playing in stdout
                            drawUI("[INFO] " + "Currently playing PSA.")
                            time.sleep(waittime/1000)

                            pass
                            break # Break out of statement
                        except (RuntimeError, TypeError, NameError, OSError, FileNotFoundError):
                            pass # Repeat
                
                # Increase chance to play PSA next time
                if psachance > 2:
                    psachance -= 1

                # Play random radio sound after speaking if file exists
                if radiosoundcount >= 1:
                    sound = mixer.Sound(str(maindirectory) + "/Assets/SoundEffects" + str(customlocation) + "/" + str(radiosound_dict[random.randint(0,radiosoundcount)]))
                    sound.set_volume(0.3)
                    mixer.Channel(2).play(sound, fade_ms=50)
                    waittime = (sound.get_length()*1000)/2
                    if waittime < 0:
                        waittime = sound.get_length()*1000
                    time.sleep(waittime/1000)
            except (RuntimeError, TypeError, NameError, OSError, KeyError, IndexError, LookupError):
                # Say that something has gone wrong
                speaktext("Something has gone wrong. Please wait while we restart the station.")
                os.execv(sys.executable, ['python3'] + sys.argv) # Restart the script by issuing a terminal command
                # os.execv(sys.executable, ['python3'] + sys.argv + ["skipintro"]) # Restart the script by issuing a terminal command, skipping the intro