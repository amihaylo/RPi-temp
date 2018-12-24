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

#The messages to be displayed to the LCD
msg1, msg2 = "test1", "test2"

#The time taken between API calls to update the weather (in seconds)
UPDATE_TIMER=900

def log(str_in):
    curr_time = str(datetime.now())
    print("{}: {}".format(curr_time, str_in))

def get_temp(city):
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location(city)
    data = location._weather_data
    condition = data["item"]["condition"]

    #RAW DUMP OF DATA
    # print(json.dumps(data, indent=2))

    # ---------TODAY---------
    city = city.upper()
    temp = condition["temp"]
    degree_sym = chr(223) + "C"
    text = condition["text"]
    date = condition["date"]
    msg = "{}: {}{} {}".format(city, temp, degree_sym, text)
    log(msg)
    return msg

def update_temps():
    global msg1
    global msg2
    msg1, msg2 = get_temp("toronto"), get_temp("sofia")    
    threading.Timer(UPDATE_TIMER, update_temps).start()

def display_temps():
    global msg1
    global msg2
    while True:
        lcd.message = msg1 + "\n" + msg2 
        for i in range(max(len(msg1), len(msg2))):
            time.sleep(0.6)
            lcd.move_left()
        
if __name__ == "__main__":
    try:
        lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
        #Make an API call to get the temperatures
        update_temps()
        #Display the temperatures
        threading.Thread(target=display_temps).start()
    except KeyboardInterrupt:
        lcd.clear()
    except:
        log("Unable to Start Thread")
