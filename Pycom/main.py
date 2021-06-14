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
        for i in range(15):
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
                    return
                else:
                    break
        print("ListaA: ", alarms_palarm)
        
        alarms_palarm.pop(index)
        alarms_palarm.append( PAlarm(10, timemark, weekly, blinkLED, addAlarm) )
        print("ListaD: ", alarms_palarm)

def removeAlarm(timemark: tuple):
    index = -1
    with alarms_lock:
        for a in alarms_palarm:
            index+=1
            if a.getSchedule() == timemark:
                break

        al = alarms_palarm.pop(index)
        al.cancelAlarm()


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
        except:
            pass

def initiate():

    print("Initiating...")
    # DS18B20 data line connected to pin P10
    ow = OneWire(Pin('G16'))
    d = DS18X20(ow)

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
        #create message
        d.start_conversion()
        time.sleep(1)
        """ temperature=10
        #temperature = d.read_temp_async()
        print(temperature)
        msg = (int(temperature*100)).to_bytes(4, 'little') """

        type = 3
        day = 6
        hour = 24
        min = 60
        ########
        payload_meta = 0
        payload_meta |= ( type << 14 )
        print(payload_meta)

        payload_meta |= ( day << 11 )
        print(payload_meta)

        payload_meta |= ( hour << 6 )
        print(payload_meta)

        payload_meta |= ( min << 0 )
        msg = payload_meta.to_bytes(2, 'little')
        print(msg)
        
        pycom.rgbled(0x0000ff)
        s.send(msg)

        #rest for a while
        time.sleep(30)

def setClock():

            #   Y   M   D   H   m
    rtc.init((2021, 6, 14, 12, 20, 0, 0, 0))    # Has to be updated every run :D

    print(rtc.now())
    print(utime.gmtime())

    print("...........")
    print(utime.mktime(rtc.now()) - utime.mktime((2021, 6, 14, 12, 21, 0, 0, 0)))
    
    print("Lista: ", alarms_palarm)
    a = PAlarm( utime.mktime((2021, 6, 14, 12, 21, 0, 0, 0)) - utime.mktime(rtc.now()), (4,15,30), False, blinkLED, addAlarm)
    alarms_palarm.append(a)
    print("Lista: ", alarms_palarm)

if __name__ == "__main__":
    pycom.heartbeat(False)

    setClock()
    #initiate()
