from collections import deque
import array
from micropython import const
from NMEA0183_Parsing import NMEA0183
from TrueWind import calcTrueWind

TWD_ARRAY_SIZE = const(30) # Rolling average base = 30 seconds.


calcTrueWind = calcTrueWind()

_RawNMAAqueue = deque((),10)
_TrueWindDirection = array.array('i', (0 for _ in range(TWD_ARRAY_SIZE)))
_TrueWindSpeed = array.array('i', (0 for _ in range(TWD_ARRAY_SIZE)))


class RcvdMsgQueue:
    def add(self, nmsg:str):
        _RawNMAAqueue.append(nmsg) # add right

    def hasMsgs(self)-> bool:
        return len(_RawNMAAqueue) > 0

    def pop(self)-> str:
        try:
            return _RawNMAAqueue.popleft() #remove left
        except:
            return "EMPTY"

class TrueWindAveraging:
    """
    Rolling average for True Wind data.
    """
    def add(self, counter: int, angle:int, speed:int):
        _TrueWindDirection[counter% TWD_ARRAY_SIZE] = angle 
        _TrueWindSpeed[counter% TWD_ARRAY_SIZE] = speed 
        
    def avgTWD(self):
        return int(sum(_TrueWindDirection)/TWD_ARRAY_SIZE) 

    def avgTWS(self):
        return int(sum(_TrueWindSpeed)/TWD_ARRAY_SIZE) 

class DisplayData:
    BoatSpeed = 0.0
    Heading = 1.1
    ApparentWindAngleCloseHaul = 2.13
    TrueWindSpeed = 4
    TrueWindDirection = 5
    DisplayMode = "upwind"
    _TWDcounter = 0
    nmea_queue = RcvdMsgQueue()
    nmea = NMEA0183()
    trueWindAveraging = TrueWindAveraging()

     # run through the Received NMEA messages queue and parse out the data
    def CalcCurrentValues(self):
        while self.nmea_queue.hasMsgs():
            self.nmea.processSentance(self.nmea_queue.pop())

        self.BoatSpeed = self.nmea.data_gps['speed']
        self.Heading = self.nmea.data_gps['track']
        awa360 = self.nmea.data_weather['wind_angle'] #NEED TO MAKE +/- 0

        if awa360 > 180:
            self.ApparentWindAngleCloseHaul = -(awa360-360)
        else:
            self.ApparentWindAngleCloseHaul = awa360

        print("self.ApparentWindAngleCloseHaul", self.ApparentWindAngleCloseHaul)

        if self.ApparentWindAngleCloseHaul < 60:
            self.DisplayMode = "upwind"
        else:
            self.DisplayMode = "downwind"

        aws = self.nmea.data_weather['wind_speed']

        if aws > 0.0:
            tws, twd = calcTrueWind.calc(awa360, aws, self.Heading, self.BoatSpeed)
            self._TWDcounter += 1
            self.trueWindAveraging.add(self._TWDcounter, twd, tws)
            self.TrueWindDirection = self.trueWindAveraging.avgTWD() 
            self.TrueWindSpeed = self.trueWindAveraging.avgTWS()




