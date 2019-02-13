from anthill import *
import time
from evdev import InputDevice, ecodes
from multiprocessing import Process, Value


# čtení z idetifikace
def get_next_card():
    device = InputDevice("/dev/input/event0")
    input_id = ""
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            input_id += str(event.code)
        if input_id.endswith("2828"):
            return input_id

def zapis_lcd(dict_key, t_delta):
    hours_format = "%H:%M:%S"
    # key_name = ups[dict_key]["name"]
    # key_status = ups[dict_key]["status"]
    # key_time = ups[dict_key]["time"]
    # hodin, zbytek = divmod(t_delta, 3600)
    # minut, vterin = divmod(zbytek, 60)
    # if key_status == "IN":
    #     s1 = ("{}, byl{}s venku".format(key_name, ups_pohlavi[dict_key]))
    # elif key_status == "OUT":
    #     s1 = ("{}, byl{}s doma".format(key_name, ups_pohlavi[dict_key]))
    # s2 = ("{}H {}M {}S!!".format(int(hodin), int(minut), int(vterin)))
    # top 4 posledni uzivatele


def zapis_txt(user_key):
    time_format = "%W %j %A %d.%m.%Y %H:%M:%S"
    name = anthill[user_key].name
    status = anthill[user_key].status
    time = anthill[user_key].time
    f = open('anthill_inout_log.txt', "a")
    f.write("{} {} {}\n".format(names, status , time.strftime(time_format, key_time)))
    f.close()


def setup(file_name='anthill_inout_log.txt'):
    parse_time_format = "%W %j %A %d.%m.%Y %H:%M:%S"
    with open(file_name) as fn:
        for row, log_txt in enumerate(fn):
            parse_line = log_txt.strip().split(" ")
            parse_name = parse_line[0]
            parse_status = parse_line[1]
            time_log = " ".join(parse_line[2:])
            parse_time_raw = time.strptime(time_log, parse_time_format)
            if parse_name in anthill:
                print(parse_name)
                # user_key = anthill[parse_name]
                # anthill[user_key].status = parse_status
                # anthill[user_key].name = parse_time_raw


# aktualizovat čas uživatele
def new_time(user_key, t_new):
    anthill[user_key].time = t_new

def timer(user_key):
    user_time = anthill[user_key].time
    print(user_time)
    t = time.mktime(time.localtime())
    t_new = time.mktime(user_time)
    t_delta = t - t_new
    t_new = time.localtime()
    return t_new, t_delta


def inout(input_id):
    if anthill[input_id].status == 'IN':
        anthill[input_id].status = 'OUT'
    elif anthill[input_id].status == 'OUT':
        anthill[input_id].status = 'IN'


def loop():
    while True:
        # input_id = input("kdo jsi?:")
        input_id = get_next_card()
        print(input_id) #aby se vědělo jaká karta se pípla
        if input_id in anthill:
            t_new, t_delta = timer(input_id)
            new_time(input_id, t_new)
            inout(input_id)
            zapis_txt(input_id)
        else:
            continue


if __name__ == "__main__":
    setup()
    loop()