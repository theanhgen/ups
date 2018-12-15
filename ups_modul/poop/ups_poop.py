#!/usr/local/bin/python

import time
import requests
from phue import Bridge

hue_toilet = 4

b = Bridge('192.168.1.202')
b.connect()

poop_ip = "http://213.227.138.203:5555/update_poop"

def poop_zapis_on(time_on):
	with open(poop_log, "a") as fp:
		fp.write("POOP ON {}\n".format(time.strftime(time_format, time.localtime(time_on))))

def poop_zapis_off(time_off):
	with open(poop_log, "a") as fp:
		fp.write("POOP OFF {}\n".format(time.strftime(time_format, time.localtime(time_off))))	  

def poop_timer(time_on):
	t2 = time.time()
	t_delta = t2 - time_on
	print("kadil jsi {0:.2f}s".format(t_delta))
	time.sleep(0.01)
	return t2

def zapis_cloud(poop_status):
    '''
    this funtion takes one parameter
    :param poop_status: either 0 or 1. 0 means no one is pooping, 1 means someone is pooping
    Depending on poop_status, it will send a message to be stored in the cloud
    you should call this function once when someone starts using the WC and once when
    someone stops using the wc
    '''
    if poop_status == 0:
        payload = "No one is pooping right now"
    else:
        payload = "toilet is currently taken" 
    requests.post(poop_ip, data=payload)

time_format = "%d.%m.%Y %H:%M:%S"
poop_log = "poop_log.txt"

#get light status from hue bridge about the light from toilet
def get_light_status():
    if b.get_light(hue_toilet, 'on') == True:
        light_status = 1
    else:
        light_status = 0
    return light_status

poop_status = 0

# Main loop
while True:
    time.sleep(0.5)
    light_status = get_light_status()
    if light_status == 1 and poop_status == 0:
        t1 = time.time()
        poop_zapis_on(t1)
        poop_status = 1
        zapis_cloud(poop_status)
    elif light_status == 0 and poop_status == 1:
        t2 = poop_timer(t1)
        poop_zapis_off(t2)
        poop_status = 0
        zapis_cloud(poop_status)

