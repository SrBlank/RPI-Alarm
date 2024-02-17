# RPI-Alarm
**2024 Update:** I will be updating this project throughout this semester with hopefully the goal of at least one commit a day. I will be updating this project as part of learning better web development practices as part of my internet software development course.

This Flask web application is designed to run on your local network and provides a convenient solution for setting alarms. The application utilizes a dedicated computer connected to speakers, allowing you to set alarms from any device. The timer, button, or sensor can be used to turn off the alarm.

The HC-SR04 sensor is used to detect movement and turn off the alarm. The sensor sends a POST request to the computer running the Flask server, and the sensor code is run on an ESP32. The button used to turn off the alarm can be a GPIO button or a keyboard button, offering flexible options for your setup. The timer will turn off the alarm by default if no button or sensor is found. The code is cross-platform and has been tested on both Windows and Ubuntu operating systems.

## Purpose
In Spring 2021 I had two 8am finals. Although I trust myself to wake up, it has happened multiple times where I've slept through my alarms. So when the time came around I plugged my laptop into a set of speakers and used the Windows Alarm App to blast my alarm. I have since used this set up multiple times so I can use my time through out the day better. 

The following semester I took a Software Engineering class where we developed multiple Flask Web Apps. I had the idea half way through the semester that I could use what I have learned in the course to my advangtage. Hence, I started working on this project to make the laptop speaker solution setup more permarnent. 

## Setting up and Running Server
Clone the repository onto the computer you want hosting the server. Then install the Python3 requirments by doing:

```bash
pip3 install -r requirments.txt
```

Next in `/RPI-Alarm/src/` create a `.env` file with a variable called `app_secret` and set it equal to anything. This is for Flask to support certain functions.

Finally start the web server by running `python3 web_server.py`. You will see two address one that is `127.0.0.1:5000` and another that will also have the `:5000` suffix. The second address is the address you will want to use on other devices to connect to the server and set alarms.

## Setup Button
Using using these [instructions](https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/) you will be able to set up a button to your raspberry pi. In `/src/alarm.py` change the `GPIO_INPUT_PIN` to the PIN you will be using.

The keyboard option will always be enabled regardless of GPIO button. To change the key used to turn off the alamr navigate back to `alarm.py` and on line 46 change `pynput.keyboard.Key.esc` to whichever key you would like to use. Refernece the pynput docs [here](https://pynput.readthedocs.io/en/latest/keyboard.html) for more key configurations.

## Setup Sensor
The code has been tested and ran on an ESP32 and an HC-SR04 sensor, these setup instructions may not work for other boards or sensors. 

Start by following the instructions [here](https://randomnerdtutorials.com/esp32-hc-sr04-ultrasonic-arduino/) to connect your sensor to your ESP32. Once that is setup download and install Arduino IDE. Then follow these [instructions](https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/) to set up your Arduino IDE. Once setup open `/Arduino/ESP32-Alarm.ino` and change the following

- `PROXIMITY` should be any number slighly less than the distance to the closest wall as to not spam request.
- `ssid` to your networks SSID (this is just the name of your network), 
- `password` to your networks password
- `host` this is the IP Address of your computer running Flask
- `port` this is the port your Flask app is running on, `5000` by default
- `trigPin` based on board, default `5` for ESP32
- `echoPin` based on board, default `18` for ESP32

Once the changes have been made plug and your ESP32 is plugged in, press the upload button in the IDE. You will eventually see the terminal saying `Connecting......` when you see this prompt press the BOOT buttton on the ESP32. The terminal should then write to the board and your sensor is setup. Before disconnecting the board, you can test to see if it works by looking at serial output `115200`. If everything looks good, your sensor is setup.

## Adding More Alarms
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

- ~~Implement HC-SR04 Sensor~~ 
- ~~Add keyboard as button input~~ 
- not doing - ~~Setting to change what key is used to intterupt~~
- ~~Validation for end user to avoid using linux features on windows, vice versa~~
- Working on alarm system using HC-SR04
- Maybe - Add a volume slider 
- Maybe - test alarm button to see how loud alarm is
- Maybe - improve Web App API

## Challenges 
As mentioned earlier the Software Engineering course taught me how to make full statck web applications. However this project deemed to be signifigantly more difficult. Some of the things I struggled with was CSS, Java Script, and the best way to implement what is now alarm.py. I believe there are many ways to improve on my approach to this project. When I first started developing, I just wanted it to be something quick and easy I could use to wake up early. However, very quickly I got invested in the project and kept adding complexties to it. Looking back I should have planned the project out, I had to redo several parts of the project. One example of this is the Alarm object. From the start I should have treated each alarm as an object however instead I had multiple lists interacting with each other making the code confusing and unreadble. Changing the code to use the Alarm class could have been worse but I think implenting an object from the start would have made my life easier all together. I was also very intimaded by Java Script when I began development as we did not use it in my Software Engineering course. I did not understand what it was for or how it could be used. I started implementing Java Script towards the end of the project and regret not using it more throughout. 

All in all, this project gave me many full stack learning experiences. I gained more confidence in HTML, CSS, Javascript, and Python as well as got to experience using an Arudino for the first time. I also found it cool that I was able to use what I learned in class to make something useful to me that I can see myself using on a daily basis. This project has already been helping me be more productive with the day and I am glad I proved to myself that I am capable of building a project like this.


