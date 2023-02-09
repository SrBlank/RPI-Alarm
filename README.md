# RPI-Alarm
Our Flask web application is designed to run on your local network and provides a convenient solution for setting alarms. The application utilizes a dedicated computer connected to speakers, allowing you to set alarms from any device. The timer, button, or sensor can be used to turn off the alarm.

The HC-SR04 sensor is used to detect movement and turn off the alarm. The sensor sends a POST request to the computer running the Flask server, and the sensor code is run on an ESP32. The button used to turn off the alarm can be a GPIO button or a keyboard button, offering flexible options for your setup. The timer will turn off the alarm by default if no button or sensor is found. The code is cross-platform and has been tested on both Windows and Ubuntu operating systems.


## Setting up and Running Server
Clone the repository onto the computer you want hosting the server. Then install the Python3 requirments by doing:

```bash
pip3 install -r requirments.txt
```

Next in `/RPI-Alarm/src/` create a `.env` file with a variable called `app_secret` and set it equal to anything. This is for Flask to support certain functions.

Finally start the web server by running `python3 web_server.py`. You will see two address one that is `127.0.0.1:5000` and another that will also have the `:5000` suffix. The second address is the address you will want to use on other devices to connect to the server and set alarms.

## Setup Button
Using using these [instructions](https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/) you will be able to set up a button to your raspberry pi. As of now the pins used in the link are the same ones used in this project.

## Setup Sensor
The code has been tested and ran on an ESP32 and an HC-SR04 sensor, these setup instructions may not work for other boards or sensors. 

Start by following the instructions [here](https://randomnerdtutorials.com/esp32-hc-sr04-ultrasonic-arduino/) to connect your sensor to your ESP32. Once that is setup download and install Arduino IDE. Then follow these [instructions](https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/) to set up your Arduino IDE. Once setup open `RPI-Alarm/Arduino/ESP32-Alarm.ino` and change the following

- `ssid` to your networks SSID (this is just the name of your network), 
- `password` to your networks password
- `host` this is the IP Address of your computer running Flask
- `port` this is the port your Flask app is running on, 5000 by default

Once the changes have been made plug and your ESP32 is plugged in, press the upload button in the IDE. You will eventually see the terminal saying `Connecting......` when you see this prompt press the BOOT buttton on the ESP32. The terminal should then write to the board and your sensor is setup.

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

