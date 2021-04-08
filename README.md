<img src="https://github.com/PhysCorp/AutomatedRadioStation/blob/main/Icon.png" width="128" height="128">

# AutomatedRadioStation
A Radio Host that's Entirely Automated!

# Listen Now [LIVE] (Explicit):
http://listen.physcorp.com/

# Suggest Songs (Experimental):
http://radio.physcorp.com

# What is it?
[*This is a fun project for me to better understand Python!*]
PhysCorp's Automated Radio Station is a new take on auto-DJ services. The station is run entirely by computers. Unlike traditional radio stations that use an auto-DJ, this station serves to include commentary between songs like a live announcer!

# How does it work?
This software is built with Python in Visual Studio Code. The program scrapes a YouTube playlist according to the weekday and time using a headless version of Firefox through selenium. The program then plays the videos in a random order, taking care to not repeat any. Between songs, the announcer occasionally talks about the weather, time, the current playlist info, or a PSA. The program connects to several APIs to administer content, such as Openweathermap for weather info and Google Cloud Text to Speech for their high quality Wavenet voices.
Additionally, users can view the current song and playlist info, as well as suggest a YouTube link to their favorite song, through the included web dashboard! You can even run multiple instances of this software with different configurations simultaneously!

# Requirements:
This program requires that you have the following installed, as well as all the dependencies listed in requirements.txt:
Terminal >> sudo apt install firefox espeak python3-venv firefox-geckodriver ffmpeg mbrola mbrola-us2 mbrola-us3 youtube-dl

# Install Instructions:
This should be used on a Debian-based Linux distro! I haven't tested other Linux distros, as well as Windows and Mac OS! Expect *many* errors.

Prereq: Clone the repo. Terminal >> git clone https://github.com/PhysCorp/AutomatedRadioStation.git

1) Make sure Python 3.8.5+ and the additional packages are installed! Run the above command listed under Requirements!
2) Change to project directory, then use PIP to install required files. Terminal >> cd AutomatedRadioStation && python3 -m pip install -r requirements.txt
3) Configure the program using the Assets and SpeechScripts folders, as well as Playlist Info and Options. Please see Configuration Tab below. Or, simply skip to step five as the program gives you a guided tutorial upon first launch!
4) Add your API Keys from Openweathermap and Google Cloud Text to Speech to the respective files (APIKeys.json and GoogleAPIKey.json). Keys aren't required, but you will experience limited functionality.
5) Run the program! Terminal >> bash StartRadio.sh

# Configuration:
[This section is included in the Guided Tutorial when the program first launches.]
First, take a look at the program's main directory. You will see several files and folders, such as \"SpeechScripts\" and \"Assets.\" Each file has a specific purpose. First, we'll start with the Assets folder.

The Assets folder contains any audio assets for the program. Currently, you will see one folder: SoundEffects. Inside of the SoundEffects folder, you can copy and paste an unlimited number of short WAV files here, which serve as transitions between speech and music. A random sound file plays each time. If you do not wish to have any transition sounds, leave the folder empty.

Back in the main directory, we will take a look at the SpeechScripts folder. Inside of this folder, you will find four text files: FirstRunPrompts, IntroTextShort, SongEndTransitions, and SongTransitions. These files serve as pseudo-random messages that play at specific intervals of the program. Before we go further, here are the details for each of the four files. FirstrunPrompts contains all of the paragraph-length introductions for the radio show. On the other hand, IntroTextShort is a drastically shorter version of the previous file, containing small messages and reminders for listeners. SongTransitions details any transitional phrases before playing a song, while SongEndTransitions provides a brief phrase after a song has finished playback. Let's take a look at SongTransitions.txt. Each line of the text file contains a different message to be read. This program chooses a line at random and reads it to the audience. With this particular file, SongTransitions.txt, this prepends each song title with a transitional phrase, such as \"You're about to hear,\" followed by the song name. You can add an unlimited number of lines to each text file, which increases the variety of speech on air.

Back in the main directory again, we'll take a look at several files. Let's start with \"APIKeys.json.\" This file holds the keys that this program uses to make API calls. Currently, there is only one entry: OpenWeatherMap. If you wish to hear about weather info, such as current conditions and temperature, copy and paste your OpenWeatherMap key in the double quotes in this file. If you wish to obtain a key, visit \"https://openweathermap.org/api\" for more info.

Now, we'll take a look at the file titled \"GoogleAPIKey.json.\" This file holds your Google API key for use with their WaveNet voices. If you wish to use WaveNet for high quality, realistic voices, search on the internet for obtaining a Cloud Console API Key. Just letting you know, Google Cloud charges a fee per every million characters that you call. Once you have your Cloud Console Key, simply REPLACE this file with your JSON key, being sure to name the file \"GoogleAPIKey.json.\"

Next, we'll take a look at the Python file titled \"PlaylistSearch.py.\" Here, you can edit which playlists this program uses, as well as when the playlist should play. Around line 22 of the file, you will see several blocks of text. Self weekdaynum represents the day of the week, starting with zero being Monday and six being Sunday. Find the appropriate block of text that you wish to edit for a specific day of the week. Inside of that specific block of text, you'll see five separate playlists. These five playlists activate at specific times throughout the day, referenced by self timeofdaynum. The first link plays from midnight to 8 AM, the second from 8 to noon, the third from noon to four, the fourth from four to eight at night, and the fifth from eight to midnight of the next day. Please edit any playlist links accordingly.

In the same file, we'll discuss setting playlist titles. Around line 107, you'll see a similar layout with each block of text, referenced by weekday and time of day. Here, each return statement is a separate line that this script reads when announcing the current playlist. For whichever playlists you modified, continue to change the text accordingly, keeping in mind the weekday and time of day numbers.

Now, we're almost done. We'll take a look at the most important file, \"Options.json.\" This file contains all of the program's options. Upon opening the file in your text editor, you'll see a range of different preferences, such as suggestions and max song length. Please edit the values accordingly. I'll describe each option here first. Playintro states whether you want to have the program give its long introduction before starting song playback. Suggestions states whether you want users to visit the associated website and suggest YouTube links to songs to be played live. Normalize audio serves to make all songs the same perceived volume. This function currently causes a memory leak, but greatly improves the quality of the radio. The port option allows you to specify which port the web server will run on. Dashboard serves to beautify the terminal output when monitoring the station. Offline mode serves to limit the number of YouTube and API calls that the program makes. Max song length sets the maximum allowable length that a song can play for. This helps to prevent pesky 24 hour loop songs from taking up the radio. The next few options describe modifying the wavenet voice, if you provided an API key earlier. Wavenet can be toggled here. Wavenet pitch modifies the voice pitch, while Wavenet speed modifies the speed accordingly. Next, wavenet voice allows you to choose the specific voice profile to use, while wavenet backup voice allows you to choose a second, lower cost, voice to use in radio downtime. That's it for wavenet options. Next, predownload is a very useful option that should be enabled when running the radio for the first time, but isn't required. This option downloads an entire YouTube playlist to your hard drive ahead of time, greatly reducing the latency between playing songs. After that, waitforuser allows this program to wait until you press enter before starting the radio. The next few options control how often a radio event occurs. For each of the following items, you can assign an arbitrary number. The higher the value, the less likely an item will play. Default PSA Chance refers to how often a public service announcement plays. Default Weather Chance refers to how often a weather report will be given. Default Welcome Chance refers to how often the radio intro will replay. Default Weekday Chance refers to how often the current playlist title will be mentioned. Finally, Default Time Chance refers to how often the current time will be mentioned. We're nearly done! Only a few more options. Next, scrolling limit is a useful option to force the web scraping engine to scroll down and gather more videos in a playlist. Set the number according to approximately how many times you need to scroll down in a playlist to see every thumbnail. For example, if there's 400 videos in a playlist on average, set this option to 4. Next, city name refers to the city name for OpenWeatherMap weather info. After that, override playlist allows you to set one single playlist to play all the time on the radio. Writeoutput and Write song info are deprecated options to write the current announcer voice lines and song info to a text file for use in programs like OBS Studio if livestreaming. Finally, PSA playlist URL allows you to set a YouTube playlist full of public service announcements to play on the air.

Thanks for taking the time to set up this software with the guided tutorial! If you wish to get more creative, check out some of the other files in the main directory here. You can even modify how the announcer reads weather info, have multiple stations with different configurations run at the same time, or adjust the layout of the website on this program's web server. [More info coming soon!]

# Current Known Issue(s):
- Audio normalizing causes a memory leak
- Song suggestions don't have a title
- Multiple instances of the webserver cannot run at the same time

<img src="https://github.com/PhysCorp/AutomatedRadioStation/blob/main/frame.png" width="128" height="128">
