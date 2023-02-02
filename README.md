# RPI-Alarm
This is a flask web server that can be ran on any linux computer that is then connected to a speaker. The user will be able to access the web server and set alarms which the server will then execute when it is time.

## Installiation 
---
## Setup up Button
Using using these [instructions](https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/) you will be able to set up a button to your raspberry pi. As of now the pins used in the link are the same ones used in this project.

## Setting up and Running Server
Clone the repository onto the computer you want hosting the server. Then install the Python3 requirments by doing:

```bash
pip3 install -r requirments.txt
```

You will also need to install `mpg123` to play `.mp3` files. Install this by running the command below in the terminal:

```bash
sudo apt install mpg321
```

Next in `/RPI-Alarm/src/` create a `.env` file with a variable called `app_secret` and set it equal to anything. This is for Flask to support certain functions.

Finally start the web server by running `python3 web_server.py`. You will see two address one that is `127.0.0.1:5000` and another that will also have the `:5000` suffix. The second address is the address you will want to use on other devices to connect to the server and set alarms.

## Configurations

### Adding More Alarms

Alarms must be of `.mp3` extension to play by default. To install new alarms either download .mp3 files or use youtube-dl to download your own from youtube. To use youtube-dl download it with the command below:

```bash
sudo pip3 install youtube-dl
```

Then find a youtube video you would like to make a mp3 of, copy its link and paste it into the command below. Run this command in `/src/alarm_sounds`.

```bash
youtube-dl --extract-audio --audio-format mp3 <youtube link>
```
Finally open `alarm.py` and change the const variable `ALARM_TO_PLAY` to the alarm that was just downloaded. It might be easier to change the name of the file downloaded as youtube-dl creates long file names.

## Future Features

This project is still a WIP. I have implemented this code on my RPI4 and I am currently testing it. The core functionality works and is waking me up on a daily basis. Below is a list of feautres I plan to add.

- Beautify Website
    - ~~Show current time~~
        - ~~java script~~
    - ~~Show next alarm to be played~~
        - ~~java script~~
    - ~~Make check boxes bigger or have them as JS switches~~
    - Add an edit alarm button
    - ~~Signify submission~~
        - ~~flask flashes?~~
    - ~~Maybe show what mp3 file will be played~~
- Code
    - ~~Add a nap button which will create an alarm that will play in X min~~
    - ~~Add button intterupt~~
    - Add days of the week for alarms
    - Add keyboard input as button 
    - ~~Have listfile.data not be overwritten every time~~
    - ~~Implement alarm class for customizability~~
        - ~~Different alarm sound for different alarms?~~
        - ~~Set up days for alarms?~~
    - ~~Create a config file~~ 
        - ~~Alarm playblack time~~
        - ~~Directory?~~
        - ~~Add alarms?~~
    - ~~Clean up alarm file~~
- ~~Turn off Alarm~~
    - ~~Timer~~
    - ~~Button~~
    - Sensor
        - Ultrasonic Sensor HC-SR04
    



