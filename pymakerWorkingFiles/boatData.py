from collections import deque
import array
from micropython import const
from NMEA0183_Parsing import NMEA0183
from TrueWind import calcTrueWind

TWD_ARRAY_SIZE = const(30) # Rolling average base = 30 seconds.
CH_ARRAY_SIZE = const(3) # Rolling average base = 3 seconds.

calcTrueWind = calcTrueWind()

_RawNMAAqueue = deque((),10)
_TrueWindDirection = array.array('i', (0 for _ in range(TWD_ARRAY_SIZE)))
_TrueWindSpeed = array.array('i', (0 for _ in range(TWD_ARRAY_SIZE)))
_ApparentWindAngleCloseHaul = array.array('f', (0 for _ in range(CH_ARRAY_SIZE)))

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
    _counter = 0
    nmea_queue = RcvdMsgQueue()
    nmea = NMEA0183()
    trueWindAveraging = TrueWindAveraging()
    utc = ""

     # run through the Received NMEA messages queue and parse out the data
    def CalcCurrentValues(self):
        
        self._counter += 1
        
        while self.nmea_queue.hasMsgs():
            self.nmea.processSentance(self.nmea_queue.pop())

        self.BoatSpeed = self.nmea.data_gps['speed']
        self.Heading = self.nmea.data_gps['track']
        self.utc = self.nmea.data_gps['utc']
        awa360 = self.nmea.data_weather['wind_angle'] #NEED TO MAKE +/- 0

        if awa360 > 180:
            _ApparentWindAngleCloseHaul[self._counter% CH_ARRAY_SIZE] = -(awa360-360)
        else:
            _ApparentWindAngleCloseHaul[self._counter% CH_ARRAY_SIZE] = awa360

        # smooth out the last 3 readings
        self.ApparentWindAngleCloseHaul = (sum(_ApparentWindAngleCloseHaul)/CH_ARRAY_SIZE) 

        if self.ApparentWindAngleCloseHaul < 90:
            self.DisplayMode = "upwind"
        else:
            self.DisplayMode = "downwind"

        # print(f"awa360: {awa360}, awaCH: {self.ApparentWindAngleCloseHaul}, bh: {self.Heading}, displayMode: {self.DisplayMode}")

        aws = self.nmea.data_weather['wind_speed']

        if aws > 0.0:
            tws, twd = calcTrueWind.calc(awa360, aws, self.Heading, self.BoatSpeed)
            self.trueWindAveraging.add(self._counter, twd, tws)
            self.TrueWindDirection = self.trueWindAveraging.avgTWD() 
            self.TrueWindSpeed = self.trueWindAveraging.avgTWS()




