from machine import Timer
from machine import Pin
import utime
import const
import socket
from luand import encodePayload

class PAlarm:

    def __init__(self, waiting_period: int, schedule: tuple, weekly_flag: bool, colorChange: function, callBack: function, pin : Pin, ssocket: socket):
        print("Alarm Created!!")
        self.schedule = schedule    # tuple (day, hour, min)
        self.weekly = weekly_flag
        self.colorChange = colorChange
        self.callBack = callBack
        self.pin = pin  
        self.ssocket = ssocket
                                                    
        self.__alarm = Timer.Alarm(self._seconds_handler, waiting_period, periodic=True)

    def _seconds_handler(self, alarm):
        start_time = utime.time()
        break_cond = False
        tolerance_time = 60 * 20 # seconds
        while not break_cond:
            self.colorChange()
            diff_time = utime.time() - start_time
            if diff_time > tolerance_time:
                print("Past Tolerance Time", diff_time)
                break_cond = True
            elif self.pin() == 1:   # Note: 1 means detecting, 0 elsewise
                print("Slot has been Openned!!")
                break_cond = True
                                                                                                                            # send 0 if > tolerance_time, so it doens't overflows
        payload = (const.INFO, self.schedule[0], self.schedule[1], self.schedule[2], const.ON_TIME if diff_time < tolerance_time else const.FORGOT, diff_time if diff_time < tolerance_time else 0)
        print("Sending: ", payload)
        self.ssocket.send( encodePayload(*payload).to_bytes(3, 'little') )
        
        if not self.weekly:
            self.cancelAlarm()
            self.callBack(self.schedule, self.ssocket, True)
    
    def cancelAlarm(self):
        self.__alarm.cancel()

    def getSchedule(self):
        return self.schedule

    def isWeekly(self):
        return  self.weekly
