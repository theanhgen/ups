import time
from anthill_data import *
from evdev import InputDevice, ecodes
from multiprocessing import Process, Value
import requests

user_fn_dict = {}

# cteni z karty
def get_next_card():
    device = InputDevice("/dev/input/event0")
    result = ""
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            result += str(event.code)
        if result.endswith("2828"):
            return result


def novy_cas(dict_key, t_alfa):
    ups[dict_key]["time"] = t_alfa

def zapis(dict_key, t_delta):
    hours_format = "%H:%M:%S"
    key_name = ups[dict_key]["name"]
    key_status = ups[dict_key]["status"]
    key_time = ups[dict_key]["time"]
    hodin, zbytek = divmod(t_delta, 3600)
    minut, vterin = divmod(zbytek, 60)
    if key_status == "IN":
        s1 = ("{}, byl{}s venku".format(key_name, ups_pohlavi[dict_key]))
    elif key_status == "OUT":
        s1 = ("{}, byl{}s doma".format(key_name, ups_pohlavi[dict_key]))
    s2 = ("{}H {}M {}S!!".format(int(hodin), int(minut), int(vterin)))
    # top 4 posledni uzivatele


def zapis_txt(dict_key):
    time_format = "%W %j %A %d.%m.%Y %H:%M:%S"
    key_name = ups[dict_key]["name"]
    key_status = ups[dict_key]["status"]
    key_time = ups[dict_key]["time"]
    f = open('inout_0.4.txt', "a")
    f.write("{} {} {}\n".format(key_name, key_status , time.strftime(time_format, key_time)))
    f.close()


def setup(file_name='inout_0.4.txt'):
    parse_time_format = "%W %j %A %d.%m.%Y %H:%M:%S"
    with open(file_name) as fn:
        for row, log_txt in enumerate(fn):
            parse_line = log_txt.strip().split(" ")
            parse_name = parse_line[0]
            parse_status = parse_line[1]
            time_log = " ".join(parse_line[2:])
            parse_time_raw = time.strptime(time_log, parse_time_format)
            if parse_name in ups_member_card:
                key_card = ups_member_card[parse_name]
                ups[key_card]["status"] = parse_status
                ups[key_card]["time"] = parse_time_raw
                update_top_4(parse_name)
    zapis_cloud()

def loop():
    while True:
        # input_card = input("kdo jsi?:")
        input_card = get_next_card()
        print(input_card) #aby se vědělo jaká karta se pípla
        if input_card in ups:
            if ups[input_card]["status"] == "IN":
                ups[input_card]["status"] = "OUT"
            elif ups[input_card]["status"] == "OUT":
                ups[input_card]["status"] = "IN"
            if input_card in ups_member_callback_dict:
                for fn in ups_member_callback_dict[input_card]:
                    fn(ups[input_card])
            zapis(input_card, t_delta)
        else:
            continue



if __name__ == "__main__":
    setup()
    loop()
