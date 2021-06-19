from machine import Timer
from machine import Pin
import utime
import const
import socket

class PAlarm:

    def __init__(self, waiting_period: int, schedule: tuple, weekly_flag: bool, colorChange: function, callBack: function, pin : Pin, ssocket: socket):
        self.seconds = 0
        self.schedule = schedule    # tuple (day, hour, min)
        self.weekly = weekly_flag
        self.colorChange = colorChange
        self.callBack = callBack
        self.pin = pin  
        self.ssocket = socket
                                                    # TODO: por waiting period
        self.__alarm = Timer.Alarm(self._seconds_handler, 30, periodic=True)

    def _seconds_handler(self, alarm):
        self.seconds += 1
        print("%02d alarm's cicles have passed" % self.seconds)
        start_time = utime.time()
        break_cond = False
        tolerance_time = 10 # seconds
        while not break_cond:
            self.colorChange()
            print("psica pisca")
            diff_time = utime.time() - start_time
            if diff_time > tolerance_time:  # TODO: por 30 minutos? ou 3h (A)
                print("Past Tolerance Time", diff_time)
                break_cond = True
            elif self.pin() == 0:   # TODO: verificar de 0 ou 1
                print("Slot has been Openned!!")
                break_cond = True
                                                                                                                            # send 0 if > tolerance_time, so it doens't overflows
        payload = (const.INFO, self.schedule[0], self.schedule[1], self.schedule[2], const.ON_TIME if diff_time < tolerance_time else const.FORGOT, diff_time if diff_time < tolerance_time else 0)
        print("Sending: ", payload)
        self.ssocket.send(payload)
        
        if not self.weekly:
            self.cancelAlarm()
            self.callBack(self.schedule, True)
    
    def cancelAlarm(self):
        self.__alarm.cancel()

    def getSchedule(self):
        return self.schedule

    def isWeekly(self):
        return  self.weekly
