#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO

import serial
import time

ser = serial.Serial('/dev/ttyUSB2',115200)
ser.flushInput()

power_key = 6
rec_buff = ''
rec_buff2 = ''
time_count = 0

def send_at(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01 )
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(command + ' ERROR')
            print(command + ' back:\t' + rec_buff.decode())
            return 0
        print(rec_buff.decode())
        return 1
    print('GPS is not ready')
    return 0

def get_gps_position():
    rec_null = True
    answer = 0
    print('Start GPS session...')
    rec_buff = ''
    send_at('AT+CGPS=0','OK',1)     # Power off GPS module
    time.sleep(1)
    send_at('AT+CGPSHOT', 'OK', 1)  # Config hot start
    time.sleep(1)
    send_at('AT+CGPS=1,2','OK',1)   # Power on GPS module
    time.sleep(1)
    while rec_null:
        answer = send_at('AT+CGPSINFO','+CGPSINFO: ',1) # Get GPS info
        if 1 == answer:
            answer = 0
            if ',,,,,,' in rec_buff:
                print('GPS is not ready')
                rec_null = False
                time.sleep(1)
        else:
            print('error %d'%answer)
            rec_buff = ''
            send_at('AT+CGPS=0','OK',1)
            return False
        time.sleep(0.5)
        ans2 = send_at('AT+CGNSSINFO', '+CGNSSINFO: ', 1) # Get GNSS info
        if 1 == ans2:
            ans2 = 0
            if ',,,,,,' in rec_buff:
                print('GPS is not ready')
                rec_null = False
                time.sleep(1)
        else:
            print('error %d'%answer)
            rec_buff = ''
            send_at('AT+CGPS=0','OK',1)
            return False
        time.sleep(2.5)


def power_on(power_key):
    print('SIM7600X is starting:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(power_key,GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(20)
    ser.flushInput()
    print('SIM7600X is ready')

def power_down(power_key):
    print('SIM7600X is loging off:')
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(3)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(18)
    print('Good bye')

try:
    power_on(power_key)
    get_gps_position()
    power_down(power_key)
except:
    if ser != None:
        ser.close()
    power_down(power_key)
    GPIO.cleanup()
if ser != None:
    ser.close()
    GPIO.cleanup()	