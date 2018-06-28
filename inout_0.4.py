import time
from ups_byt_test import *
top_4 = []

file = open("inout_0.4_test.txt", "a")
file.close()


def casovac(dict_key):
	key_time = ups[dict_key]["time"]
	t = time.mktime(time.localtime())
	t_alfa = time.mktime(key_time)
	t_delta = t - t_alfa
	t_alfa = time.localtime()
	return t_alfa, t_delta


def novy_cas(dict_key, t_alfa):
	ups[dict_key]["time"] = t_alfa


def zapis(dict_key, t_delta):
	key_name = ups[dict_key]["name"]
	key_status = ups[dict_key]["status"]
	key_time = ups[dict_key]["time"]
	hour, remain = divmod(t_delta, 3600)
	minutes, seconds = divmod(remain, 60)
	if key_status == "IN":
		print("{}, byl{}s venku".format(key_name, ups_pohlavi[dict_key]))
	elif key_status == "OUT":
		print("{}, byl{}s doma".format(key_name, ups_pohlavi[dict_key]))
	print("{}H {}M {}S!!".format(int(hour), int(minutes), int(seconds)))
	# top 4 posledni uzivatele
	if key_name in top_4:
		top_4.remove(key_name)
	top_4.append(key_name)
	if len(top_4) > 4:
		top_4.pop(0)
	for x in reversed(range(len(top_4))):
		list_name = top_4[x]
		hours_format = "%H:%M:%S"
		member_card = ups_member_card[list_name]
		member_status = ups[member_card]["status"]
		member_time = ups[member_card]["time"]
		if x == 3:
			last = "*"
		else:
			last = ""
		print("{:<6} {:<3} {}{}".format(list_name, member_status, time.strftime(hours_format, member_time), last))


def zapis_txt(dict_key):
	time_format = "%W %j %A %d.%m.%Y %H:%M:%S"
	key_name = ups[dict_key]["name"]
	key_status = ups[dict_key]["status"]
	key_time = ups[dict_key]["time"]
	file = open("inout_0.4_test.txt", "a")
	file.write("{} {} {}\n".format(key_name, key_status , time.strftime(time_format, key_time)))
	file.close()


file_name = 'inout_0.4_test.txt'
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

			
while True:
	input_card = input("kdo jsi?:")
	if input_card in ups:
		t_alfa, t_delta = casovac(input_card)
		novy_cas(input_card, t_alfa)
		if ups[input_card]["status"] == "IN":
			ups[input_card]["status"] = "OUT"
		elif ups[input_card]["status"] == "OUT":
			ups[input_card]["status"] = "IN"
		zapis(input_card, t_delta)
		zapis_txt(input_card)
	else:
		print("neznamy clovek \n ALARM")
