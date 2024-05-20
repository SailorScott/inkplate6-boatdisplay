import math

class calcTrueWind: 
    # From Seatalk MWV message
    # awa = 320.0  # 0 to 359
    # aws = 20.0 # knots

    # # From GPS RMC message
    # bh = 180.0 # GPS track
    # bs = 10.0 # GPS speed in knots

    def calc(self, awa:float, aws:float, bh:float, bs:float):
        """
        Calculate true wind speed and direction based on boat speed and heading, apparant wind angle and speed.
        Inputs: awa - apparent Wind Angle from Seatalk Wind Instruments
                aws - Apparent Wind Speed "
                bh - Boat Heading from GPS
                bs - Boat Speed from GPS
        Returns:
            float: tws, twd True Wind Speed and Direction as tuple
        """
        awaOrig = awa

        if awa > 180: # Seatalk ST60 puts out 0 to 360 for relative heading.
            awa = awa-360

        # http://www.sailnet.com/forums/general-discussion-sailing-related/50411-apparent-wind-formula.html
        # with modifications
        awa1 = awa
        if (awa < 0):
            awa1 = -awa

        Y = 90-awa1
        a = aws*math.cos(Y*math.pi/180)
        bb = aws*math.sin(Y*math.pi/180)
        b = bb-bs
        tws = round(math.sqrt((a*a)+(b*b)))
        twa = 90-(math.atan(b/a)*180/math.pi)
        if (awa < 0):
            twa = -twa
        
        twd = round((twa+bh)%360)
        # print(f"bh={bh:.1f}, bs={bs:.1f}, awa={awaOrig:.1f}, aws={aws:.1f}, tws={tws}, twd={twd}")
        return tws, twd
