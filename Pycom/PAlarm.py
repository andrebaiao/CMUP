from machine import Timer

class PAlarm:

    def __init__(self, waiting_period: int, schedule: tuple, weekly_flag: bool, colorChange: function, callBack: function):
        self.seconds = 0
        self.schedule = schedule    # tuple (day, hour, min)
        self.weekly = weekly_flag
        self.colorChange = colorChange
        self.callBack = callBack
        self.__alarm = Timer.Alarm(self._seconds_handler, 9, periodic=True)

    def _seconds_handler(self, alarm):
        self.seconds += 1
        print("%02d seconds have passed" % self.seconds)
        self.colorChange()
        if not self.weekly:
            self.cancelAlarm() # stop counting after 10 seconds
            self.callBack(self.schedule, True)
    
    def cancelAlarm(self):
        self.__alarm.cancel()

    def getSchedule(self):
        return self.schedule

    def isWeekly(self):
        return  self.weekly
