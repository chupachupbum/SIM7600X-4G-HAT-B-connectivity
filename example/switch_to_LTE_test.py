"""
This script will switch off wifi for a moment then let Raspberry Pi auto
connect to LTE. After that, call an API and save log.
"""
import requests
import time
import os


cmd_wifi_off = 'ifconfig wlan0 down'
cmd_wifi_on = 'ifconfig wlan0 up'

url = "https://api.adviceslip.com/advice"

try:
    os.system(cmd_wifi_off)
    time.sleep(5)
except Exception:
    print("Failed to turn off WiFi")


for i in range(3):
    with open('log.txt', 'a') as file:
        try:
            response = requests.request("GET", url, timeout=5)

            print(response.text)
            file.write(response.text + '\n')
            time.sleep(5)

        except Exception:
            print("Disconnected!")
            file.write("Disconnected...\n")
    i+=1

time.sleep(5)
try:
    os.system(cmd_wifi_on)
    time.sleep(5)
except Exception:
    print("Failed to turn on WiFi")
