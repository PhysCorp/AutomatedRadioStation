<img src="https://github.com/PhysCorp/AutomatedRadioStation/blob/main/Icon.png" width="128" height="128">
# AutomatedRadioStation
A Radio Host that's Entirely AI-Generated!

# What is it?
PhysCorp's Automated Radio Station is a new take on auto-DJ services. The station is run entirely by computers. Unlike traditional radio stations that use an auto-DJ, this station serves to include commentary between songs like a live announcer!

# How does it work?
This software is built with Python in Visual Studio Code. The program scrapes a YouTube playlist according to the weekday, using a headless version of Firefox. The program then plays the videos in a random order, taking care to not repeat videos in headless VLC instance. Between songs, the announcer occasionally talks about the weather, the current playlist info, or a PSA.

# Requirements
This program requires that you have the following installed, as well as all the dependencies listed in requirements.txt:
firefox, espeak, python3-venv, firefox-geckodriver

Advanced speech synthesis requires Real-Time-Voice-Cloning by blue-fish
https://github.com/blue-fish/Real-Time-Voice-Cloning

<img src="https://github.com/PhysCorp/AutomatedRadioStation/blob/main/frame.png" width="128" height="128">
