<img src="https://github.com/PhysCorp/AutomatedRadioStation/blob/main/Icon.png" width="128" height="128">

# AutomatedRadioStation
A Radio Host that's Entirely AI-Produced!

# What is it?
[This is a fun project for me to better understand Python!]
PhysCorp's Automated Radio Station is a new take on auto-DJ services. The station is run entirely by computers. Unlike traditional radio stations that use an auto-DJ, this station serves to include commentary between songs like a live announcer!

# How does it work?
This software is built with Python in Visual Studio Code. The program scrapes a YouTube playlist according to the weekday, using a headless version of Firefox. The program then plays the videos in a random order, taking care to not repeat videos in headless VLC instance. Between songs, the announcer occasionally talks about the weather, the current playlist info, or a PSA.

# Requirements:
This program requires that you have the following installed, as well as all the dependencies listed in requirements.txt:
firefox, espeak, python3-venv, firefox-geckodriver

Advanced speech synthesis requires Real-Time-Voice-Cloning by blue-fish
https://github.com/blue-fish/Real-Time-Voice-Cloning

# Install Instructions:
This should be used on a Debian-based Linux distro!

Prereq: Clone the repo. Terminal: "git clone https://github.com/PhysCorp/AutomatedRadioStation.git"

1) Make sure Python 3.8.5+ and the additional packages are installed! Terminal: "sudo apt install python3 python3-pip firefox firefox-geckodriver python3-venv espeak"
2) Change to project directory, then use PIP to install required files. Terminal: "cd AutomatedRadioStation && pip3 install -r requirements.txt"
*Optionally, use PIP to install required files for voice synthesis. Terminal: "pip3 install -r requirements_voice.txt"
3) Configure any speech scripts/playlists (See "Configuration Tab Below").
4. Run the program! Terminal: "python3 Main.py"

# Configuration:
+ Sound Effects are stored in Assets/SoundEffects. Place any .WAV files in that directory, then rename the file to a number (Example: "1.WAV"). The radio will play a random sound effect before the announcer speaks.
+ Radio scripts are stored in the "Speech Scripts" folder. "IntroTextShort.txt" accounts for all the brief welcome messages. "FirstrunPrompts.txt" holds all of the lengthy introductions to the radio segment.
*Add more lines to either file to increase variety.

# Known Issue(s):
- None ATM!

<img src="https://github.com/PhysCorp/AutomatedRadioStation/blob/main/frame.png" width="128" height="128">
