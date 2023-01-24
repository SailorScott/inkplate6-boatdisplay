
import time
import uasyncio
import network
from machine import I2C

import screen_display
import screen_setup
from inkplate import *
from dgram import UDPServer
import boatData 

port = 2000

Inkplate.init(I2C(0, scl=Pin(22), sda=Pin(21)))
ipm = InkplateMono()
ipp = InkplatePartial(ipm)

screen = screen_setup.screen_setup(ipm)
display = screen_display.screen_display(screen)
displayData = boatData.DisplayData()

# Connect to local Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('SVMorePractice', 'T0G0Faster!')
    while not wlan.isconnected():
        print('Trying to connect...')
        pass
print('network config:', wlan.ifconfig())


async def DisplayUpdater():
    """
    Every second, reads the current data and sends to display elements.
    """
    lastDisplayMode = ""

    while True:
        t0 = time.ticks_ms()
        displayData.CalcCurrentValues()


        displayMode = displayData.DisplayMode # "downwind"  or "upwind"
        
        if lastDisplayMode != displayMode:
            ipm.clear()
            ipm.display()
            lastDisplayMode = displayMode

        displaySpeed = displayData.BoatSpeed

        ipp.start()
        if displayMode == "downwind":
            ipm._framebuf[:] = screen.downWindBackground[:]
            displayCompass = displayData.Heading

        else:
            ipm._framebuf[:] = screen.upWindBackground[:]
            displayCompass = displayData.ApparentWindAngleCloseHaul #Heading



        display.BoatSpeed(ipm, displaySpeed)
        display.AngleLine(ipm, displayCompass, displayMode)
        display.TrueWind(ipm, displayData.TrueWindDirection, displayData.TrueWindSpeed)
        await uasyncio.sleep_ms(125)
        ipp.display()

        drawTime_ms = time.ticks_diff(time.ticks_ms(), t0)
        print("Draw: in %dms" % drawTime_ms)
        nextWake = 1000-drawTime_ms
        if nextWake < 10:
            nextWake = 10
        await uasyncio.sleep_ms(nextWake)


def main():
    loop = uasyncio.get_event_loop()
    udpReceiver = UDPServer()

    loop.create_task(DisplayUpdater())
    loop.run_until_complete(udpReceiver.serve('192.168.0.255', port)) # anything on the local network on port


 

main()
