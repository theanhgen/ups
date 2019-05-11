from anthill import *
from inout_gsheet import *
import time
from evdev import InputDevice, ecodes
from multiprocessing import Process, Value


# setup of the script with parsing the log
def setup(file_name='/github/ups_anthill/ups_modul/inout/anthill_inout_log.txt'):
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
        if parse_status == "IN":
            anthill_name[parse_name].day_in = parse_time_raw[2]
        # print(anthill_name[parse_name].name, anthill_name[parse_name].status, anthill_name[parse_name].time, anthill_name[parse_name].day_in)

# parse the old list that is created after each iteration with the input ID
def parse_backup_list(file_name='/github/ups_anthill/ups_modul/inout/anthill_list.txt'):
    old_list = []
    with open(file_name) as fn:
        for row, log_txt in enumerate(fn):
            parse_line = log_txt.strip().split(" ")
            parse_name = parse_line[0]
            old_list.append(parse_name)
    return old_list

# compares two lists and returns a list of tuples
# each tuple contains (name, "removed"/"added", it's index)
def compare_lists(old_list, anthill_list):
    changes = []
    set_l1 = set(old_list)
    set_l2 = set(anthill_list)
    # ^ .. symmetric set difference
    diff = set_l1 ^ set_l2
    for x in diff:
        if x in old_list:
            change_location = old_list.index(x)
            changes.append((x, change_location, "removed"))
        elif x in anthill_list:
            change_location = anthill_list.index(x)
            changes.append((x, change_location, "added"))
    changes.sort(key = lambda changes: changes[1])
    return changes

# delete the old users rows
def delete_row(changes):
    for (x,y,z) in reversed(changes):
        if z == "removed":
            print("smazat", x ,y)
            row_detele(y, wks)

# add new users rows
def insert_row(changes):
    for (x,y,z) in changes:
        if z == "added":
            print("pridat", x, y)
            row_insert(y, wks)

# check the list whether new user was added
# the whole checking new users and deleting and adding
def check_new_users(wks):
    old_list = parse_backup_list()
    changes = compare_lists(old_list, anthill_list)
    delete_row(changes)
    insert_row(changes)
    names_rows(wks)

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

def hours_IN(t_delta):
    hours = float(t_delta / 3600)
    return hours

# update user with new time
def new_time(user_key, t_new):
    anthill_card[user_key].time = t_new

# inout switch
def inout(input_id, user_name, hours, wks):
    if anthill_card[input_id].status == 'OUT':
        day = time.localtime()
        anthill_card[input_id].day_in = day.tm_mday
        day_in = anthill_card[input_id].day_in
        print(day_in)
        anthill_card[input_id].status = 'IN'
    elif anthill_card[input_id].status == 'IN':
        day_in = anthill_card[input_id].day_in
        user_time_log(day_in, user_name, hours, wks)
        anthill_card[input_id].status = 'OUT'

# logging the user data to txt log
def log_txt(user_key):
    time_format = "%W %j %A %d.%m.%Y %H:%M:%S"
    user_name = anthill_card[user_key].name
    user_status = anthill_card[user_key].status
    user_time = anthill_card[user_key].time
    f = open('/github/ups_anthill/ups_modul/inout/anthill_inout_log.txt', "a")
    f.write("{} {} {}\n".format(user_name, user_status , time.strftime(time_format, user_time)))
    f.close()

# using the ID dict to get the username
def id_name(input_id):
    user_name = anthill_card[input_id].name
    return user_name

# write a list of current anthill empployyes after each ittereation with input ID
def backup_list():
    f = open('/github/ups_anthill/ups_modul/inout/anthill_list.txt', "w")
    for x in range(len(anthill_list)):
        user_name = anthill_list[x]
        f.write("{}\n".format(user_name))
    f.close()

# main loop waiting for an user ID. updating user data
def loop():
    while True:
        # input_id = input("kdo jsi?:")
        input_id = get_next_card()
        print(input_id) #print the ID to console. for adding new user
        if input_id in anthill_card:
            wks, new_month, days_range = new_month_sheet()
            user_name = id_name(input_id)
            t_new, t_delta = timer(input_id)
            hours = hours_IN(t_delta)
            new_time(input_id, t_new)
            inout(input_id, user_name, hours, wks)
            log_txt(input_id)
            backup_list()
        else:
            continue

# weird stuff
if __name__ == "__main__":
    setup()
    # check_new_users()
    loop()
