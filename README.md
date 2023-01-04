# RPI-Alarm
This is a flask web server that can be ran on any linux computer that is then connected to a speaker. The user will be able to access the web server and set alarms which the server will then execute when it is time.

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


### Changing Alarm Playtime

Navigate to `alarm.py` in `/src/` and change the const variable `ALARM_PLAYTIME` to an integer. This will play the alarm for a number of seconds.

## Future Features

- Beautify Website
    - Signify submission 
        - flask flashes?
    - Show current time
        - java script
    - Show next alarm to be played
        - java script
    - Maybe show what mp3 file will be played
- Code
    - Have listfile.data not be overwritten every time
    - Create a config file
        - Alarm playblack time
        - Directory?
        - Add alarms?
    - Clean up alarm file
    - Different alarm sound for different alarms?
    - Set up days for alarms?
- Turn off Alarm
    - Timer
    - Button
    - Sensor
    
## Disclaimer
This project is still a WIP. The code runs locally as far I have tested it and the next step is to test it on the RPI since the develeopment has been on my laptop in WSL. Below is a list of things I must do before I am able to develop this project further.
1. ~~Set up RPI~~
2. ~~Buy a router~~
    - ~~Since the apartments internet I think restricts hosting servers~~ 
    - ~~Still need to look into this~~
3. Find a solution to having two audio outputs from two computers into one speaker
    - This is so I can have my desktop and RPI use the same speaker
4. Integrate and test


