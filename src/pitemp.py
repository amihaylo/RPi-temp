# -*- coding: utf-8 -*-
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import threading
import json
import requests
import os
from binascii import hexlify
from datetime import datetime

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)

lcd_columns = 16
lcd_rows = 2

#Define the cities that will be cycled to display
cities = ["toronto", "sofia", "bogota"]

#DO NOT EDIT: this is where results for the api calls are stored
results = [None]*len(cities)

#The path to the log file
LOG_FILENAME="./pitemp.log"

#The time taken between API calls to update the weather (in seconds)
UPDATE_TIMER=600

def log(str_in):
    curr_time = str(datetime.now())
    #Remove any newlines for easier logging
    str_in = str_in.replace("\n", " | ")
    log_msg = "[{}]: {}".format(curr_time, str_in)
    print(log_msg)
    with open(LOG_FILENAME, "a") as logfile:
        logfile.write(log_msg + "\n")

def get_temp(city):
    try:
        WEATHERAPIKEY = os.environ['WEATHERAPIKEY']
        data = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}'.format(city, WEATHERAPIKEY)).json()

        # print(json.dumps(data, indent=2))
        city = city.capitalize()
        temp = data["main"]["temp"]
        degree_sym = chr(223) + "C"
        desc = data["weather"][0]["description"].capitalize()
        msg = "{}: {}{}\n{}".format(city, temp, degree_sym, desc)
    except KeyError:
        msg = "ERROR: ENVIRONMENT VAR NOT FOUND"
    log(msg)
    return msg
        
def update_temps():
    global results
    for i,city in enumerate(cities):
        results[i] = get_temp(city)
    threading.Timer(UPDATE_TIMER, update_temps).start()

def display_temps():
    global results
    while True:
        for city_msg in results:
            lcd.message = city_msg
            time.sleep(5)
            lcd.clear()
        
if __name__ == "__main__":
    try:
        lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
        #Give it enough time to connect to initialize
        lcd.message = "Loading..."
        time.sleep(10)
        
        #Make an API call to get the temperatures
        update_temps()
        #Display the temperatures
        threading.Thread(target=display_temps).start()
    except KeyboardInterrupt:
        lcd.backlight = False
        lcd.clear()
    except Exception as e:
        log(e)
