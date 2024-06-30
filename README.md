# VoiceAssistant

[![Python version](https://img.shields.io/badge/python-3.8-blue.svg)](https://python.org)

This application is a voice assistant for fulfilling user requests and communicating with him using machine learning and neural networks. A set of neural networks is used for speech recognition and synthesis, recognition of user emotions by camera or speech, etc.

## Features
### Time
Using the phrases "ctime" from the config file you can find out the current system time.

### News
Using the phrase "news" from the config file, the assistant will open a site with news.

### Weather
Using the phrase "weather" from the config file, the assistant will announce the current weather in the specified city.

### Music
Using music control phrases such as "start_music", "stop_music", "pause_songs", "continue_songs", "next_song", "previous_song", "reduce_songs", "increase_songs", "more_reduce_songs", "more_increase_songs", you can play the music, stop it, change the volume or switch it.

### Chess
Using the phrase "play_chess" you can play chess with an assistant.

### Emotion Recognition
Also, the assistant, using pre-trained neural networks, can recognize emotions based on the user’s photo or phrases.

### Menu
By calling up the assistant menu, you can control it without using your voice. In the menu you can perform all the same actions as with your voice, but in addition, in the menu you can change the name of the assistant, choose which side to play in chess and control the player more conveniently.

## Setup
1. Install Python 3.8.
2. During the setup, tick Install launcher for all users (recommended) and Add Python 3.8 to PATH when prompted.
3. Install Git for Windows.
4. During the setup, tick Git from the command line and also 3rd-party software, Checkout Windows-style, commit Unix-style endings, and Use MinTTY (the default terminal MSYS2).
5. Open Git Bash by right-clicking an empty space inside of a folder (e.g My Documents) and clicking Git Bash here.
6. Run git clone https://github.com/xarals/VoiceAssistant.git VoiceAssistant -b master in the command window that opens.
7. Download files [camera_emotion_model.h5](https://drive.google.com/file/d/1_YbzmTirB0i-HlYG0J7tpq8x5zsP0xDa/edit), [model_small](https://drive.google.com/file/d/1LsRk8wSwqDKnDYd8eXyHDcIYPgWA8Csg/view) then unpack into the resulting directory.
8. Run main.py in Windows command line interpreter.
