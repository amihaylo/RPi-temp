# RPI TEMPERATURE DISPLAY 
#### Using an RPI and a char LCD displays the current temperature, and updates it periodically through python weather API

# Instructions
1. `sudo apt-get update`
2. `sudo apt-get -y install python3-pip`
3. `pip3 install -r requirements.txt`
4. `make`

# Hardware Used
1. [Raspberry Pi 3 Model B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
>  ![Raspberry Pi 3 Model B+](./res/img/rpi3_bplus.jpg)
2. [Standard HD44780 LCD](https://www.adafruit.com/product/181)
>  ![Standard HD44780 LCD](./res/img/lcd_16x2.jpg)

# Schematic
`TODO`

# To run on RPi startup
1. `crontab -e`
2. Append to end of the file : `@reboot python3 <path>/src/pytemp.py`
3. Replace `<path>` with the full pathname of the repo
4. `sudo reboot`
