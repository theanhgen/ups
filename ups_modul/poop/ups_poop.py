#!/usr/local/bin/python
import time
import requests
from phue import Bridge
from ups_keys import *


# conenct to HUE. press the button on the bridge
def connect_HUE(bridge_ip):
    b = Bridge(bridge_ip)
    b.connect()
    return b

# loggin to txt when poop is on
def poop_on_log(time_on):
    with open(poop_log, "a") as fp:
        fp.write("POOP ON {}\n".format(time.strftime(time_format, time.localtime(time_on))))

# logging to txt when the poop is off
def poop_off_log(time_off):
    with open(poop_log, "a") as fp:
        fp.write("POOP OFF {}\n".format(time.strftime(time_format, time.localtime(time_off))))

# poop timer. print to console
def poop_timer(time_on):
    t2 = time.time()
    t_delta = t2 - time_on
    print("někdo kadil {0:.2f}s".format(t_delta))
    return t2, t_delta

#get light status from hue bridge. the toiler light (actually the light socket)
def get_light_status(b):
    if b.get_light(hue_toilet, 'on') == True:
        light_status = 1
    else:
        light_status = 0
    return light_status

# pushing the poop info to cloud, so people can check with sirir shortcuts
def cloud_log(poop_status):
    if poop_status == 0:
        payload = "No one is pooping right now"
    else:
        payload = "toilet is currently taken" 
    requests.post(poop_ip, data=payload)

# authenficate using OAuth
def authenficate():
    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

# divider for the hours, minutes and seconds
def se_mi_ho(t_delta):
    hours, se_mi = divmod(t_delta, 3600)
    minutes, seconds = divmod(se_mi, 60)
    return hours, minutes, seconds

# setting the string to push the tweet
def poop_tweet(hours, minutes, seconds):
    poop_tweet_time = "someone pooped for {}H {}M {:.2f}S".format(int(hours), int(minutes), seconds)
    return poop_tweet_time

# pushing the tweet to twitter
def push_tweet(poop_tweet_time):
    authenficate()
    api.update_status(poop_tweet_time)


poop_status = 0
b = connect_HUE(bridge_ip)
api = authenficate()


# main loop with sleep time 0.5 seconds
# def poop_loop():
while True:
    time.sleep(0.5)
    light_status = get_light_status(b)
    if light_status == 1 and poop_status == 0:
        t1 = time.time()
        poop_on_log(t1)
        # cloud_log(poop_status)
        poop_status = 1
    elif light_status == 0 and poop_status == 1:
        t2, t_delta = poop_timer(t1)
        poop_off_log(t2)
        # cloud_log(poop_status)
        hours, minutes, seconds = se_mi_ho(t_delta)
        poop_tweet_time = poop_tweet(hours, minutes, seconds)
        push_tweet(poop_tweet_time)
        poop_status = 0
