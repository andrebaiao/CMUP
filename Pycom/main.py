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

""" Setup Variables - Must be Set/verified before every run """
                #   Y    M   D   H   m
setup_start_time = (2021, 6, 14, 12, 20, 0, 0, 0)
setup_time_slots = {(0, 12,30) : Pin('P10', mode = Pin.IN), (0,18,30) : Pin('P9', mode = Pin.IN)} # <weekday [0-6 / mon-sun], hour [0-23], minute [0-60]>

""" Global Vars """
rtc = RTC()

color_lock = _thread.allocate_lock()
alarms_lock = _thread.allocate_lock()

alarms_palarm = []

""" Shared Region """
def changeLED(color):
    with color_lock:
        pycom.rgbled(color)

def blinkLED():
    with color_lock:
        for _ in range(5):
            pycom.rgbled(0xff0000)
            time.sleep(0.4)
            pycom.rgbled(0x888888)
            time.sleep(0.1)
        pycom.rgbled(0x000000)


def addAlarm(timemark: tuple, weekly = False):
    print("Adding :D")
    index = -1
    with alarms_lock:
        for a in alarms_palarm:
            index+=1
            if a.getSchedule() == timemark:
                if a.isWeekly():
                    return False
                else:
                    break
        print("ListaA: ", alarms_palarm)

        t_pin = None
        for times in sorted(setup_time_slots.keys()):
            if timemark[0] == times[0] and 0 <= timemark[1] - times[1] <= 3:
                print("fica: ", times, setup_time_slots[times])
                t_pin = setup_time_slots[times]
                break
        
        if not t_pin:
            return False
        
        alarms_palarm.pop(index)    # TODO: por seconds of a week
        alarms_palarm.append( PAlarm(10, timemark, weekly, blinkLED, addAlarm, t_pin) )
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
def threadWork():
    sct = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sct.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    sct.bind(1)
    sct.setblocking(True)
    #sct.settimeout(30)
    while True:
        try:
            print("Receiving...")
            msg = sct.recv(64)
            print("got", msg)

            #interpret data
            data = int.from_bytes(msg, 'little')
            print("msg: ", data)

            # check if slot available before creating alarm (maybe send confirmation msg?)
        except:
            pass

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

    _thread.start_new_thread(threadWork, ())

    while True:
        time.sleep(1)

        type = 3
        day = 6
        hour = 24
        min = 60

        msg = luand.encodePayload(type, day, hour, min, 1).to_bytes(3, 'little')

        print(msg)
        
        pycom.rgbled(0x0000ff)
        s.send(msg)

        #rest for a while
        time.sleep(30)

def setClock():

    rtc.init(setup_start_time)

    print(rtc.now())
    print(utime.gmtime())

    print("...........setup_start_time = (2021, 6, 14, 12, 20, 0, 0, 0)")
    print(utime.mktime((2021, 6, 14, 12, 21, 0, 0, 0)) - utime.mktime(rtc.now()))
    return
    print("Lista: ", alarms_palarm)
    a = PAlarm( utime.mktime((2021, 6, 14, 12, 21, 0, 0, 0)) - utime.mktime(rtc.now()), (0,15,30), False, blinkLED, addAlarm, setup_time_slots[(0, 12,30)])
    
    alarms_palarm.append(a)
    print("Lista: ", alarms_palarm)

if __name__ == "__main__":
    pycom.heartbeat(False)

    print("Initiating...")
    setClock()
    #initiate()
