from micropython import const


class screen_display:
    # NUM locations work left to right, smallest value to top/right of display.
    # 1st line Boat speed line 150px tall, space 210
    LINE1 = const(20)
    LINE1NUM1 = const(30)
    LINE1NUM2 = const(240)
    LINE1NUM3 = const(425)
    # 2nd line - GPS Heading or Apparant Wind Angle 
    # 150 x tall, space 210
    LINE2 = const(300)
    LINE2NUM1 = const(30)
    LINE2NUM2 = const(240)
    LINE2NUM3 = const(425)
    # 3rd line - True wind speed and 
    # 90 px tall, space 100
    LINE3 = const(570)
    LINE3NUM1 = const(30)
    LINE3NUM2 = const(130)
    LINE3NUM3 = const(230)
    LINE3NUM4 = const(390)
    LINE3NUM5 = const(490)

    # 4th line - True Wind angle, target speed target angle, battery level
    #  display.TargetVPP(ipm, 123, 4.5, 178) # twa, tbs, tba
    # 40 px tall, right to left, space 50
    LINE4 = const(737)
    # tba
    LINE4NUM1 = const(30)
    LINE4NUM2 = const(80)
    LINE4NUM3 = const(130)
    # tbs
    LINE4NUM4 = const(220)
    LINE4NUM5 = const(280)
    LINE4NUM6 = const(330)
    # twa
    LINE4NUM7 = const(440)
    LINE4NUM8 = const(500)
    LINE4NUM9 = const(550)

    _HasLowBattery = False

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
        # print("AngleLine:", str(angle))
        if displayMode == 'downwind':
            displayAngle = "{:0>3}".format(int(angle*1.0))
        else:
            displayAngle = "{:0>3}".format(int(angle*10.0))

        ipm.blit(self.screen.NumLookupLarge(displayAngle[0]), LINE2, LINE2NUM3)
        ipm.blit(self.screen.NumLookupLarge(displayAngle[1]), LINE2, LINE2NUM2)
        ipm.blit(self.screen.NumLookupLarge(displayAngle[2]), LINE2, LINE2NUM1)
        return ipm

    def TrueWind(self, ipm, twd, tws):
        # True Wind Angle - 0 to 359
        displayTWD = "{:0>3}".format(twd)

        ipm.blit(self.screen.NumLookupSmall(displayTWD[0]), LINE3, LINE3NUM3) #Xxx
        ipm.blit(self.screen.NumLookupSmall(displayTWD[1]), LINE3, LINE3NUM2) #xXx
        ipm.blit(self.screen.NumLookupSmall(displayTWD[2]), LINE3, LINE3NUM1) #xxX

        # True Wind Speed - only 2 digits
        displayTWS = "{:0>2}".format(tws)
        if displayTWS[0] != "0":
            ipm.blit(self.screen.NumLookupSmall(displayTWS[0]), LINE3, LINE3NUM5)
        ipm.blit(self.screen.NumLookupSmall(displayTWS[1]), LINE3, LINE3NUM4)

        return ipm

    def TargetVPP(self, ipm, twa, tbs, tba):
        # Left to right TWA  123 , Target Boat Speed, 12.3, Target Boat Angle 123

        displayTWA = "{:0>3}".format(twa)
        ipm.blit(self.screen.NumLookupSmallest(displayTWA[0]), LINE4, LINE4NUM3) #Xxx
        ipm.blit(self.screen.NumLookupSmallest(displayTWA[1]), LINE4, LINE4NUM2) #xXx
        ipm.blit(self.screen.NumLookupSmallest(displayTWA[2]), LINE4, LINE4NUM1) #xxX

        tbs = int(tbs * 10.0) # have fixed descimal point
        displaySpeed = "{:0>3}".format(tbs)

        if displaySpeed[0] != "0":
            ipm.blit(
                self.screen.NumLookupSmallest(displaySpeed[0]), LINE4, LINE4NUM9
            )  # Xxx
        ipm.blit(self.screen.NumLookupSmallest(displaySpeed[1]), LINE4, LINE4NUM8)  # xXx
        ipm.blit(self.screen.NumLookupSmallest(displaySpeed[2]), LINE4, LINE4NUM7)  # xxX

        # target boat angle - 3 digits, -1 = no angle.
        if tba > 0: 
            displayTBA = "{:0>3}".format(tba)
            if displayTBA[0] != "0":
                ipm.blit(self.screen.NumLookupSmallest(displayTBA[0]), LINE4, LINE4NUM6)
            ipm.blit(self.screen.NumLookupSmallest(displayTBA[1]), LINE4, LINE4NUM5)
            ipm.blit(self.screen.NumLookupSmallest(displayTBA[2]), LINE4, LINE4NUM4)

        return ipm


    def LowBattery(self, ipm):
        # Icon in top corner
        ipm.fill_triangle(120, 575, 120, 525, 220, 550, 1) 
        return ipm

    def SetBatteryState(self, state):
        self._HasLowBattery = state
    
    def GetBatteryState(self):
        return self._HasLowBattery
    