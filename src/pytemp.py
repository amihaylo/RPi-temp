# -*- coding: utf-8 -*-
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import threading
from weather import Weather, Unit
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

#The time taken between API calls to update the weather (in seconds)
UPDATE_TIMER=900

def log(str_in):
    curr_time = str(datetime.now())
    #Remove any newlines for easier logging
    str_in = str_in.replace("\n", " | ")
    print("[{}]: {}".format(curr_time, str_in))

def get_temp(city):
    try:
        weather = Weather(unit=Unit.CELSIUS)
        location = weather.lookup_by_location(city)
        data = location._weather_data
        condition = data["item"]["condition"]
    except:
        log("cloud not access API")

    #RAW DUMP OF DATA
    # print(json.dumps(data, indent=2))

    # ---------TODAY---------
    city = city.upper()
    temp = condition["temp"]
    degree_sym = chr(223) + "C"
    text = condition["text"]
    date = condition["date"]
    msg = "{}: {}{}\n{}".format(city, temp, degree_sym, text)
    log(msg)
    return msg


def update_temps():
    global results
    for i,city in enumerate(cities):
        results[i] = get_temp(city)
    threading.Timer(UPDATE_TIMER, update_temps).start()

def display_temps():
    # global results
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
