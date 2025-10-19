import time
from ups_byt import *
from write_oled import write_2l, write_4l, write_top4
from evdev import InputDevice, ecodes
from multiprocessing import Process, Value
import requests
top_4 = []
ups_cloud_update_ip = 'http://213.227.138.203:5555/update'

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


def casovac(dict_key):
    key_time = ups[dict_key]["time"]
    t = time.mktime(time.localtime())
    t_alfa = time.mktime(key_time)
    t_delta = t - t_alfa
    t_alfa = time.localtime()
    return t_alfa, t_delta


def novy_cas(dict_key, t_alfa):
    ups[dict_key]["time"] = t_alfa

def update_top_4(key_name):
    if key_name in top_4:
        top_4.remove(key_name)
    top_4.append(key_name)
    if len(top_4) > 4:
        top_4.pop(0)
    

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
    write_2l(s1, s2)
    update_top_4(key_name)
    # top 4 posledni uzivatele
    to_print = []
    for x in reversed(range(len(top_4))):
        list_name = top_4[x]
        member_card = ups_member_card[list_name]
        member_status = ups[member_card]["status"]
        member_time = ups[member_card]["time"]
        if x == 3:
            last = "*"
        else:
            last = ""
        to_print.append("{:<6} {:<3} {}{}".format(list_name, member_status, time.strftime(hours_format, member_time), last))
    write_top4(to_print)


def zapis_txt(dict_key):
    time_format = "%W %j %A %d.%m.%Y %H:%M:%S"
    key_name = ups[dict_key]["name"]
    key_status = ups[dict_key]["status"]
    key_time = ups[dict_key]["time"]
    with open("inout_0.4.txt", "a", encoding="utf-8") as file:
        file.write(f"{key_name} {key_status} {time.strftime(time_format, key_time)}\n")


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
    # zapis_cloud()

def led_loop():
    while True:
        # input_card = input("kdo jsi?:")
        input_card = get_next_card()
        print(input_card) #aby se vědělo jaká karta se pípla
        if input_card in ups:
            t_alfa, t_delta = casovac(input_card)
            novy_cas(input_card, t_alfa)
            ups[input_card]["status"] = (
                "OUT" if ups[input_card]["status"] == "IN" else "IN"
            )
            # if input_card in ups_member_callback_dict:
            #     for fn in ups_member_callback_dict[input_card]:
            #         fn(ups[input_card])
            zapis(input_card, t_delta)
            zapis_txt(input_card)
            # zapis_cloud()
        else:
            write_2l("neznamy clovek!!", "ALARM")
            continue


def zapis_cloud():
    hours_format = "%H:%M:%S"
    print("updating to cloud")
    cur_home = []
    for x in reversed(range(len(top_4))):
        list_name = top_4[x]
        member_card = ups_member_card[list_name]
        member_status = ups[member_card]["status"]
        member_time = ups[member_card]["time"]
        if member_status == "IN":
            cur_home.append((list_name, time.strftime(hours_format, member_time)))
    if len(cur_home) == 0:
        output_str = "No one is home right now!"
    else:
        output_str = "Currently there is:*"
        for res in cur_home:
            output_str += "{} ({})* ".format(res[0], res[1])
        output_str += "at home"
    print(output_str)
    requests.post(ups_cloud_update_ip, data=output_str)


if __name__ == "__main__":
    setup()
    led_loop()
