# RPI-Alarm
This is a flask web server that can be ran on any computer (in my case a Raspberry Pi 4) that is then connected to a speaker. The user will be able to access the web server and set alarms which the server will then execute when it is time.

## Run Locally
Clone the repository locally and make sure all the dependecies are installed. Create a `.env` file in `/src/` with a variable called `app_secret` and set it equal to anything. This is for Flask to support certain functions.

Then to start the web server run `python3 web_server.py`. By default you should be able to access the webpage by going to `127.0.0.1:5000` in any web browser.

## Disclaimer
This project is still a WIP. The code runs locally as far I have tested it and the next step is to test it on the RPI since the develeopment has been on my laptop in WSL. Below is a list of things I must do before I am able to develop this project further.
1. Set up RPI
2. Buy a router 
    - Since the apartments internet I think restricts hosting servers 
    - Still need to look into this
3. Find a solution to having two audio outputs from two computers into one speaker
    - This is so I can have my desktop and RPI use the same speaker
4. Integrate and test


