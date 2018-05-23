#!/usr/bin/python
#
# Python script voor testen LEDs op de sterren print "Sjouke Bedankt !!"
# 28-2-2017
#
# LED driver: PCA9685
#


import smbus
import time
import sys
import subprocess

# Functie om een LED aan te zetten met helderheid in procenten
#
# LED is PWM met een totale tijd van 4096 counts. 
# hier binnen zet je de start "on" en de stop "off"
# door de "on" te verdelen loopt er minder stroom als alle LEDs aan staan
# de "count" in 12 bit, daarom een "low" en een "high" veld

def led_on(bus, DEVICE_ADDRESS, led_nr, proc=25):
    on_count = (4095 * proc) / 100
# verdeel begin led aan over de 16 uitgangen
    start = led_nr * ((4095 - on_count)/16)
    on_low = start & 0xff
    on_high = (start & 0xf00 ) >> 8
    bus.write_byte_data(DEVICE_ADDRESS, 0x06+4*led_nr, on_low)
    bus.write_byte_data(DEVICE_ADDRESS, 0x07+4*led_nr, on_high)

# LED uit tijd berekenen.. max is 4095
    off_count = start + on_count
    off_low   = off_count & 0xff
    off_high  = (off_count & 0xf00) >> 8
    bus.write_byte_data(DEVICE_ADDRESS, 0x08+4*led_nr, off_low)
    bus.write_byte_data(DEVICE_ADDRESS, 0x09+4*led_nr, off_high)

# Functie om een LED uit te zetten
def led_off(bus, DEVICE_ADDRESS, led_nr):
    bus.write_byte_data(DEVICE_ADDRESS, 0x06+4*led_nr, 0x00)
    bus.write_byte_data(DEVICE_ADDRESS, 0x07+4*led_nr, 0x00)
    bus.write_byte_data(DEVICE_ADDRESS, 0x08+4*led_nr, 0x00)
    bus.write_byte_data(DEVICE_ADDRESS, 0x09+4*led_nr, 0x00)
    
def main():
    try :
        hat_name = subprocess.check_output("sudo cat /proc/device-tree/hat/product", shell=True)
    except:
        hat_name="no hat"
        pass

    if (hat_name[:7] != "Sterren"):
        sys.exit("Geen sterren hat geplaatst")
    

# aanmaken van de I2C bus en addressen voor de LED drivers
    bus = smbus.SMBus(1) # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1) 
    DEVICES = [] #7 bit address (will be left shifted to add the read write bit) 
    DEVICES.append(0x40)
# Ik heb maar 1 led driver... hekje weghalen voor meer led drivers
    DEVICES.append(0x41)
    DEVICES.append(0x42)
    DEVICES.append(0x43)

# Reset de LED drivers
    bus.write_byte(0x00, 0x06)

# set de led driver in de juiste mode
    for DEVICE_ADDRESS in DEVICES:    
        bus.write_byte_data(DEVICE_ADDRESS, 0x00, 0x0E)
        bus.write_byte_data(DEVICE_ADDRESS, 0x01, 0x04)

# lus om led's aan en uit te zetten.
    for loops in range(1):
        for DEVICE_ADDRESS in DEVICES:
            for led_nr in range(16):
                for helder in range(10):
                    led_on(bus, DEVICE_ADDRESS, led_nr, helder*helder)
                    time.sleep(0.02)
                led_off(bus, DEVICE_ADDRESS, led_nr)

    Grote_beer=      [[0,0,50,0,0,50,0,0,0,0,0,0,50,0,0,0],
                      [0,0,50,0,0,0,0,0,0,0,0,0,0,0,50,50],
                      [0,0,0,0,50,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    Kleine_beer =    [[50,0,0,0,0,50,0,50,0,50,0,0,0,0,0,0],
                      [50,0,0,0,0,0,0,0,50,0,0,0,0,0,0,50],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    Orion=           [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,50,50,50,0,50,0,0,50,0,0,0,0,0,0],
                      [0,50,0,0,0,0,50,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    Andromeda=       [[0,0,0,0,0,50,0,0,0,50,0,0,0,0,0,0],
                      [0,0,0,0,50,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,50,0,0,0,0,50,0,0,0],
                      [0,0,0,0,0,0,0,0,50,0,0,0,0,0,0,0]]
    Aquila=          [[30,0,60,20,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,50,0,0,0,0,0,0,0,0],
                      [0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,30,30,0,0,0,0,0,0,0,0,0,0,0,0]]
    Bootes=          [[0,0,0,50,0,0,0,0,0,0,0,0,0,0,0,0],
                      [50,0,30,0,0,50,0,0,0,0,50,50,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,60,0,0,0,0,0,50,0,0,0,0,0]]
    Cassiopeia =     [[0,0,0,0,0,50,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,50,0,0,0,0,0,0,0,0,0,50,0],
                      [0,0,0,0,0,30,0,0,50,0,0,30,0,0,0,0],
                      [0,0,0,0,0,50,0,0,0,0,0,0,0,0,0,0]]
    Ceapheus =       [[0,0,0,0,0,50,0,0,0,0,50,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,50,0,0,0],
                      [0,0,0,0,50,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,50,50,0,0]]
    Gemini =         [[0,0,0,50,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,20,0,0,0,0,0,0,0,0,0,0,0,20,20,0],
                      [0,0,0,0,0,0,0,0,0,50,0,0,0,0,0,0],
                      [0,0,0,0,0,0,50,0,0,0,0,0,0,0,0,0]]
    Pegasus =        [[0,0,0,0,0,0,50,0,0,0,0,50,0,50,0,0],
                      [0,0,0,0,0,0,50,0,0,0,0,0,0,0,0,0],
                      [50,0,0,0,0,0,0,0,0,0,50,0,0,0,0,50],
                      [0,50,0,0,0,0,0,0,0,50,0,0,0,0,0,0]]
    Voerman=          [[0,0,0,0,0,50,0,0,50,0,0,0,0,10,10,50],
                      [0,0,0,0,50,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0],
                      [0,0,50,0,0,0,0,0,0,0,0,50,0,0,0,0]]
    Zwaan =          [[0,50,0,0,0,0,0,0,0,50,0,0,0,0,0,0],
                      [0,0,50,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,50,0,0,0,0,0,0,0,0,0,0,50,50,0],
                      [50,0,0,50,0,0,50,0,0,0,0,0,0,0,0,0]]
    Trianqulum =     [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,50,0,0,0,0,0,0,0,0,50,50]]
    Leeg =           [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    Sterren_beelden=[Zwaan, Voerman, Pegasus, Gemini, Ceapheus, Cassiopeia, Bootes, 
                     Trianqulum, Aquila, Andromeda, Orion, Kleine_beer, Grote_beer, Leeg]
    while 1:
        for beeld in Sterren_beelden:
            for device_nr, DEVICE_ADDRESS in enumerate(DEVICES):
                for led_nr in range(16):
                    led_on(bus, DEVICE_ADDRESS, led_nr, beeld[device_nr][led_nr])
            time.sleep(15)

if __name__ == "__main__":
    main()
