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

The project is still a WIP. Currently development is being adjusted and tested for windows and linux based systems. Below is a list of features I want to add. I am setting these goals for myself or I will keep adding features to no end. I hope to add these features and wrap up the project by the end of Feburary 2023. 

- Implement HC-SR04 Sensor 
- Add keyboard as button input 
- Setting to change what key is used to intterupt
- Validation for end user to avoid using linux features on windows, vice versa
- Maybe - Add a volume slider 
- Maybe - test alarm button to see how loud alarm is

