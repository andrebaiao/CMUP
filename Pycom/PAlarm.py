from machine import Timer
from machine import Pin
import utime

class PAlarm:

    def __init__(self, waiting_period: int, schedule: tuple, weekly_flag: bool, colorChange: function, callBack: function, pin : Pin):
        self.seconds = 0
        self.schedule = schedule    # tuple (day, hour, min)
        self.weekly = weekly_flag
        self.colorChange = colorChange
        self.callBack = callBack
        self.pin = pin                                      # por waiting period
        self.__alarm = Timer.Alarm(self._seconds_handler, 30, periodic=True)

    def _seconds_handler(self, alarm):
        self.seconds += 1
        print("%02d alarm's cicles have passed" % self.seconds)
        start_time = utime.time()
        break_cond = False
        while not break_cond:
            self.colorChange()
            print("psica pisca")
            diff_time = utime.time() - start_time
            if diff_time > 10:
                print("passou muito tempo", diff_time)
                break_cond = True
                # TODO: mandar msg
            elif self.pin() == 0:   # TODO: verificar de 0 ou 1
                print("foi aberto")
                break_cond = True
                # TODO: mandar msg

        if not self.weekly:
            self.cancelAlarm()
            self.callBack(self.schedule, True)
    
    def cancelAlarm(self):
        self.__alarm.cancel()

    def getSchedule(self):
        return self.schedule

    def isWeekly(self):
        return  self.weekly
