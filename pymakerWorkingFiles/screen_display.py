from micropython import const


class screen_display:
    # NUM locations work left to right, smallest value to top/right of display.
    # 1st line Boat speed line
    LINE1 = const(20)
    LINE1NUM1 = const(30)
    LINE1NUM2 = const(240)
    LINE1NUM3 = const(425)
    # 2nd line - GPS Heading or Apparant Wind Angle
    LINE2 = const(300)
    LINE2NUM1 = const(30)
    LINE2NUM2 = const(240)
    LINE2NUM3 = const(425)
    # 3rd line - True wind speed and angle
    LINE3 = const(580)
    LINE3NUM1 = const(30)
    LINE3NUM2 = const(130)
    LINE3NUM3 = const(230)
    LINE3NUM4 = const(390)
    LINE3NUM5 = const(490)

    def __init__(self, screen):
        self.screen = screen # screen has the framebuffers of the number shapes.

    def BoatSpeed(self, ipm, boatSpeed:float):
        # Boat speed (GPS Speed)
        bsp = int(boatSpeed * 10.0) # have fixed descimal point
        displaySpeed = "{:0>3}".format(bsp) 

        if displaySpeed[0] != "0":
            ipm.blit(
                self.screen.NumLookupLarge(displaySpeed[0]), LINE1, LINE1NUM3
            )  # Xxx
        ipm.blit(self.screen.NumLookupLarge(displaySpeed[1]), LINE1, LINE1NUM2)  # xXx
        ipm.blit(self.screen.NumLookupLarge(displaySpeed[2]), LINE1, LINE1NUM1)  # xxX
        # return ipm

    def AngleLine(self, ipm, angle:float, displayMode):
        # Apparant Wind Angle OR GPS Heading
        # displayMode = upwind then show decimal point for AWA, offwind no decimal for heading
        if displayMode == 'downwind':
            displayAngle = "{:0>3}".format(int(angle*1.0))
        else:
            displayAngle = "{:0>3}".format(int(angle*10.0))

        ipm.blit(self.screen.NumLookupLarge(displayAngle[0]), LINE2, LINE2NUM3)
        ipm.blit(self.screen.NumLookupLarge(displayAngle[1]), LINE2, LINE2NUM2)
        ipm.blit(self.screen.NumLookupLarge(displayAngle[2]), LINE2, LINE2NUM1)
        return ipm

    def TrueWind(self, ipm, twa, tws):
        # True Wind Angle - 0 to 359
        displayTWA = "{:0>3}".format(twa)

        ipm.blit(self.screen.NumLookupSmall(displayTWA[0]), LINE3, LINE3NUM3) #Xxx
        ipm.blit(self.screen.NumLookupSmall(displayTWA[1]), LINE3, LINE3NUM2) #xXx
        ipm.blit(self.screen.NumLookupSmall(displayTWA[2]), LINE3, LINE3NUM1) #xxX

        # True Wind Speed - only 2 digits
        displayTWS = "{:0>2}".format(tws)
        if displayTWS[0] != "0":
            ipm.blit(self.screen.NumLookupSmall(displayTWS[0]), LINE3, LINE3NUM5)
        ipm.blit(self.screen.NumLookupSmall(displayTWS[1]), LINE3, LINE3NUM4)

        return ipm
