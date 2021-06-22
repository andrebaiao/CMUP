import pycom
from network import LoRa
import time
import binascii
import socket

from machine import Pin
from onewire import DS18X20
from onewire import OneWire

import _thread

from machine import RTC
import utime
from PAlarm import PAlarm
import luand
import const

""" Setup Variables - Must be Set/verified before every run """
                #   Y    M   D   H   m
setup_start_time = (2021, 6, 14, 6, 57)
setup_time_slots = {(0, 7, 0) : Pin('P10', mode = Pin.IN), (0,12, 0) : Pin('P9', mode = Pin.IN)} # <weekday [0-6 / mon-sun], hour [0-23], minute [0-60]>

""" Global Vars """
rtc = RTC()

color_lock = _thread.allocate_lock()
alarms_lock = _thread.allocate_lock()

alarms_palarm = []

""" Shared Region """
def blinkLED():
    with color_lock:
        for _ in range(5):
            pycom.rgbled(0xff0000)
            time.sleep(0.4)
            pycom.rgbled(0x888888)
            time.sleep(0.1)
        pycom.rgbled(0x000000)


def addAlarm(timemark: tuple, ssocket : socket , weekly = False):
    index = -1
    found = False
    with alarms_lock:
        for a in alarms_palarm:
            index+=1
            if a.getSchedule() == timemark:
                found = True
                if a.isWeekly():
                    return False
                else:
                    break

        t_pin = None
        for times in sorted(setup_time_slots.keys()):
            if timemark[0] == times[0] and 0 <= timemark[1] - times[1] <= 3:
                t_pin = setup_time_slots[times]
                break
        
        if not t_pin:
            return False
        
        if found:
            alarms_palarm.pop(index) 

        if weekly:                      # seconds in a week
            alarms_palarm.append( PAlarm(604800, timemark, weekly, blinkLED, addAlarm, t_pin, ssocket) )
        else:
                t_now = utime.gmtime()
                t_day = t_now[6]

                diff_days = timemark[0] - t_day
                if diff_days < 0:
                    diff_days = (7 - t_day) + timemark[0]
                                            # seconds in a day  - actually seconds                              + desired seconds
                alarms_palarm.append( PAlarm(86400 * diff_days - (t_now[3] * 3600 + t_now[4] * 60 + t_now[5]) + (timemark[1] * 3600 + timemark[2] * 60), timemark, weekly, blinkLED, addAlarm, t_pin, ssocket) )
        print("ListaD: ", alarms_palarm)
        return True

def removeAlarm(timemark: tuple):
    index = -1
    with alarms_lock:
        for a in alarms_palarm:
            index+=1
            if a.getSchedule() == timemark:
                break

        al = alarms_palarm.pop(index)
        al.cancelAlarm()

""" Threads """
""" Downlink Receiver """
def threadWork(ssocket : socket):
    sct = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sct.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    sct.bind(1)
    sct.setblocking(True)

    while True:
        try:
            print("Receiving...")
            msg = sct.recv(64)

            #interpret data
            data = int.from_bytes(msg, 'little')
            payload = luand.decodePayload(msg)
            print("Payload received: ", payload)

            if int(payload[0]) == const.SET and int(payload[4]) == const.ADD:
                addAlarm( (payload[1], payload[2], payload[3]), ssocket )

            ssocket.send( luand.encodePayload(const.VOID, 0, 0, 0, 0, 0).to_bytes(3, 'little') )
        except Exception as e:
            print("An error has ocorred:", e)

def initiate():

    lora = LoRa(mode=LoRa.LORAWAN)

    app_eui = binascii.unhexlify('70B3D57ED00421AB')    
    app_key = binascii.unhexlify('758B8247E12A37076C194B517D0999D5')

    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

    # wait until the module has joined the network
    pycom.rgbled(0xFF0000)
    while not lora.has_joined():
        time.sleep(2.5)
        print('Not joined yet... Have you registered device ID? Mine is:')
        print(binascii.hexlify(lora.mac()).upper().decode('utf-8'))

    print('Network joined!')
    pycom.rgbled(0x00FF00)

    # setup a socket to transmit data
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    s.setblocking(False)

    _thread.start_new_thread(threadWork, [s] )
    while True:
        s.send( luand.encodePayload(const.VOID, 0, 0, 0, 0, 0).to_bytes(3, 'little') )

        #rest for a arbitrary interval   
        time.sleep(60 * 30)

def setClock():

    rtc.init(setup_start_time)

    print("Actual Time: ", rtc.now())

if __name__ == "__main__":
    pycom.heartbeat(False)

    print("Initiating...")
    setClock()
    initiate()
