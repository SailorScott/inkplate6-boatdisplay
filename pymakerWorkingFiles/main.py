import random
import time

import screen_display
import screen_setup
from inkplate import *



if __name__ == "__main__":
    from machine import I2C

    Inkplate.init(I2C(0, scl=Pin(22), sda=Pin(21)))
    ipm = InkplateMono()
    ipp = InkplatePartial(ipm)

    screen = screen_setup.screen_setup(ipm)
    display = screen_display.screen_display(screen)

    # TODO
    # Screen Display for mode change between AWA vs Compass
    # Setup the second procesor thread to monitor Wi-Fi
    # Connect to local network
    # NEMA Parsing
    # State machine for checking for data, battery, mode change, refresh 
    # Calculate TWA, TWS
    # Control web page?? (LED On/off, brightness)



    iter = 0

    while True:

        ipm.clear()
        ipm.display()

        print(f"VBatt:", str(Inkplate.read_battery()))

        for i in range(1000):
            print("number:", str(i))
            displaySpeed = i  # random.randint(0, 12))
            displayCompass = random.randint(0, 359)
            displayTWA = Inkplate.read_battery() * 10.0 # random.randint(0, 359)
            displayTWS = random.randint(8, 15)
            displayMode = "upwind"  # upwind or offwind

            t0 = time.ticks_ms()
            ipp.start()
            ipm._framebuf[:] = screen.downWindBackground[:]

            ipm = display.BoatSpeed(ipm, displaySpeed)
            ipm = display.AngleLine(ipm, displayCompass, displayMode)
            ipm = display.TrueWind(ipm, displayTWA, displayTWS)

            ipp.display()

            drawTime_ms = time.ticks_diff(time.ticks_ms(), t0)
            print("Draw: in %dms" % drawTime_ms)
            sleepTime = (1000 - drawTime_ms)/1000
            time.sleep(sleepTime)
