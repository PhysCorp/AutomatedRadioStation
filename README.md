<img src="https://github.com/PhysCorp/AutomatedRadioStation/blob/main/Icon.png" width="128" height="128">

# AutomatedRadioStation
A Radio Host that's Entirely Automated!

# Listen Now [LIVE]:
http://listen.physcorp.com/

# What is it?
[*This is a fun project for me to better understand Python!*]
PhysCorp's Automated Radio Station is a new take on auto-DJ services. The station is run entirely by computers. Unlike traditional radio stations that use an auto-DJ, this station serves to include commentary between songs like a live announcer!

# How does it work?
This software is built with Python in Visual Studio Code. The program scrapes a YouTube playlist according to the weekday, using a headless version of Firefox. The program then plays the videos in a random order, taking care to not repeat videos in headless VLC instance. Between songs, the announcer occasionally talks about the weather, the current playlist info, or a PSA. The program connects to several APIs to administer content, such as Openweathermap for weather info, YouTube Data for gathering video info, and Google Cloud Text to Speech for their Wavenet voices.

# Requirements:
This program requires that you have the following installed, as well as all the dependencies listed in requirements.txt:
firefox, espeak, python3-venv, firefox-geckodriver, mbrola, mbrola-us2, mbrola-us3

Advanced speech synthesis requires Real-Time-Voice-Cloning by blue-fish
https://github.com/blue-fish/Real-Time-Voice-Cloning

# Install Instructions:
This should be used on a Debian-based Linux distro! I haven't tested other Linux distros, as well as Windows and Mac OS! Expect *many* errors.

Prereq: Clone the repo. Terminal: "git clone https://github.com/PhysCorp/AutomatedRadioStation.git"

1) Make sure Python 3.8.5+ and the additional packages are installed! Terminal: "sudo apt install python3 python3-pip firefox firefox-geckodriver python3-venv espeak mbrola mbrola-us2 mbrola-us3"
2) Change to project directory, then use PIP to install required files. Terminal: "cd AutomatedRadioStation && pip3 install -r requirements.txt"
*Optionally, use PIP to install required files for voice synthesis. Terminal: "pip3 install -r requirements_voice.txt"*
3) Configure any speech scripts/playlists (See "Configuration Tab Below").
4) Add your API Keys from Openweathermap, YouTube Data, and Google Cloud Text to Speech to the respective files (APIKeys.json and GoogleAPIKey.json). Keys aren't required, but you will experience limited functionality.
5) Run the program! Terminal: "python3 Main.py"

# Configuration:
+ Check out the Options.json file to configure the program. There, you can adjust the PSA playlist info, speech provider, and more!
+ Sound Effects are stored in Assets/SoundEffects. Place any .WAV files in that directory, then rename the file to a number (Example: "1.WAV"). The radio will play a random sound effect before the announcer speaks.
+ Waiting/Background Music is stored in Assets/Music. Place any .WAV files in that directory, then rename the file to a number (Example: "1.WAV"). The radio will play a random file when waiting or the announcer is speaking.
+ Radio scripts are stored in the "Speech Scripts" folder. "IntroTextShort.txt" accounts for all the brief welcome messages. "FirstrunPrompts.txt" holds all of the lengthy introductions to the radio segment.
*Add more lines to either file to increase variety.

# Known Issue(s):
1) You may experience issues with Pafy if you make too many YouTube API calls within 24 hours. The issue will resolve itself automatically within 24 hours.
2) The program currently does not set GOOGLE_APPLICATION_CREDENTIALS var automatically. You must manually specify the path to Google Cloud JSON file to use Wavenet voices.
3) Reading the time aloud will result in a delay according to the length of the song. This will be fixed shortly.

# License info for live playback on my server:
Intro/Wait music from Jukedeck - create your own at http://jukedeck.com

Rising Tide (faster) by Kevin MacLeod
Link: https://incompetech.filmmusic.io/song/5028-rising-tide-faster-
License: https://filmmusic.io/standard-license

Simplex by Kevin MacLeod
Link: https://incompetech.filmmusic.io/song/4367-simplex
License: https://filmmusic.io/standard-license

Seven March by Kevin MacLeod
Link: https://incompetech.filmmusic.io/song/4338-seven-march
License: https://filmmusic.io/standard-license

Secret of Tiki Island by Kevin MacLeod
Link: https://incompetech.filmmusic.io/song/4331-secret-of-tiki-island
License: https://filmmusic.io/standard-license

Professor Umlaut by Kevin MacLeod
Link: https://incompetech.filmmusic.io/song/4243-professor-umlaut
License: https://filmmusic.io/standard-license

Private Eye by Kevin MacLeod
Link: https://incompetech.filmmusic.io/song/4240-private-eye
License: https://filmmusic.io/standard-license

Prelude and Action by Kevin MacLeod
Link: https://incompetech.filmmusic.io/song/4236-prelude-and-action
License: https://filmmusic.io/standard-license

<img src="https://github.com/PhysCorp/AutomatedRadioStation/blob/main/frame.png" width="128" height="128">
