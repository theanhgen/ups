from anthill import *
import time
from evdev import InputDevice, ecodes
from multiprocessing import Process, Value


# setup of the script with parsing the log
def setup(file_name='anthill_inout_log.txt'):
    parse_time_format = "%W %j %A %d.%m.%Y %H:%M:%S"
    with open(file_name) as fn:
        for row, log_txt in enumerate(fn):
            parse_line = log_txt.strip().split(" ")
            parse_name = parse_line[0]
            parse_status = parse_line[1]
            time_log = " ".join(parse_line[2:])
            parse_time_raw = time.strptime(time_log, parse_time_format)
            setup_user(parse_name, parse_status, parse_time_raw)

# update user information from log for first run of the script
def setup_user(parse_name, parse_status, parse_time_raw):
    if parse_name in anthill_name:
        anthill_name[parse_name].status = parse_status
        anthill_name[parse_name].time = parse_time_raw

# reading the user ID
def get_next_card():
    device = InputDevice("/dev/input/event0")
    input_id = ""
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            input_id += str(event.code)
        if input_id.endswith("2828"):
            return input_id

# timer between inout
def timer(user_key):
    user_time = anthill_card[user_key].time
    t = time.mktime(time.localtime())
    t_new = time.mktime(user_time)
    t_delta = t - t_new
    t_new = time.localtime()
    return t_new, t_delta

# update user new time
def new_time(user_key, t_new):
    anthill_card[user_key].time = t_new

# inout switch
def inout(input_id):
    if anthill_card[input_id].status == 'IN':
        anthill_card[input_id].status = 'OUT'
    elif anthill_card[input_id].status == 'OUT':
        anthill_card[input_id].status = 'IN'

# logging the user data to txt log
def log_txt(user_key):
    time_format = "%W %j %A %d.%m.%Y %H:%M:%S"
    user_name = anthill_card[user_key].name
    user_status = anthill_card[user_key].status
    user_time = anthill_card[user_key].time
    f = open('anthill_inout_log.txt', "a")
    f.write("{} {} {}\n".format(user_name, user_status , time.strftime(time_format, user_time)))
    f.close()

# main loop waiting for an user ID. updating user data
def loop():
    while True:
        # input_id = input("kdo jsi?:")
        input_id = get_next_card()
        print(input_id) #print the ID to console. for adding new user
        if input_id in anthill_card:
            t_new, t_delta = timer(input_id)
            new_time(input_id, t_new)
            inout(input_id)
            log_txt(input_id)
        else:
            continue

# weird stuff
if __name__ == "__main__":
    setup()
    loop()
