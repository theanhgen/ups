import time
from ups_modul.inout.ups_byt import *
from datetime import timedelta


file_name = 'inout_0.4_test.txt'
file_parse_in = 'inout_0.4_IN.txt'
file_parse_out = 'inout_0.4_OUT.txt'


parse_time_format_old = "%W %j %A %d.%m.%Y %H:%M:%S"
parse_time_format_new = "%d.%m.%Y %H:%M:%S"


ups_heatmap = {}
for c in range(len(ups_member_card)):
	for k, v in ups_member_card.items():
			ups_heatmap[v] = {
				"name" : k,
				"time_in" : [],
				"time_out" : [],
				"time_in_delta" : [],
				"time_out_delta" : [],
				}


def time_in_delta_fc(key_card):
	time_in = ups_heatmap[key_card]["time_in"]
	time_out = ups_heatmap[key_card]["time_out"]
	time_in_delta = ups_heatmap[key_card]["time_in_delta"]
	time_out_delta = ups_heatmap[key_card]["time_out_delta"]
	for x in range(len(time_out)):
		t_in_delta = time_out[x] - time_in[x]
		t_in_delta_int = int(t_in_delta)
		time_in_delta.append(t_in_delta_int)
	for x in range((len(time_in)-1)):
		t_out_delta = time_in[x+1] - time_out[x]
		t_out_delta_int = int(t_out_delta)
		time_out_delta.append(t_out_delta_int)


def every_second_IN(keys):
	with open(file_parse_in) as fp:
		key_card = ups_member_card[keys]
		time_in = ups_heatmap[key_card]["time_in"]
		time_in_delta = ups_heatmap[key_card]["time_in_delta"]
		file = open("inout_0.4_IN.txt", "a")
		for x in range(len(time_in_delta)):
			for s in range(time_in_delta[x]//60):
				time_in_sec = int(time_in[x])
				time_in_seconds = time_in_sec + (s * 60) 
				time_in_seconds_new = time.localtime(time_in_seconds)
				time_in_seconds_parse = time.strftime(parse_time_format_old, time_in_seconds_new)
				file.write("{} {} {}\n".format(ups_heatmap[key_card]["name"].capitalize(), "IN", time_in_seconds_parse))
		file.close()

def every_second_OUT(keys):
	with open(file_parse_out) as fp:
		key_card = ups_member_card[keys]
		time_out = ups_heatmap[key_card]["time_out"]
		time_out_delta = ups_heatmap[key_card]["time_out_delta"]
		file = open("inout_0.4_OUT.txt", "a")
		for x in range(len(time_out_delta)):
			for s in range(time_out_delta[x]//60):
				time_out_sec = int(time_out[x])
				time_out_seconds = time_out_sec + (s * 60)
				time_out_seconds_new = time.localtime(time_out_seconds)
				time_out_seconds_parse = time.strftime(parse_time_format_old, time_out_seconds_new)
				file.write("{} {} {}\n".format(ups_heatmap[key_card]["name"].capitalize(), "OUT", time_out_seconds_parse))
		file.close()


file = open("inout_0.4_IN.txt", "w")
file.close()

file = open("inout_0.4_OUT.txt", "w")
file.close()


with open(file_name) as fn:
	for row, log_txt in enumerate(fn):
		parse_all = log_txt.strip().split(" ")
		parse_name = parse_all[0]
		parse_status = parse_all[1]
		time_log = " ".join(parse_all[2:])
		parse_time_raw = time.strptime(time_log, parse_time_format_old)
		parse_time_new = time.strftime(parse_time_format_new, parse_time_raw)
		if parse_name in ups_member_card.keys():
			key_card = ups_member_card[parse_name]
			time_in = ups_heatmap[key_card]["time_in"]
			time_out = ups_heatmap[key_card]["time_out"]
			time_in_delta = ups_heatmap[key_card]["time_in_delta"]
			time_out_delta = ups_heatmap[key_card]["time_out_delta"]
			if parse_status == "IN":
				time_in.append(time.mktime(parse_time_raw))
			if parse_status == "OUT":
				time_out.append(time.mktime(parse_time_raw))


for k, v in ups_member_card.items():
	time_in_delta_fc(v)


for keys in ups_member_card.keys():
	every_second_IN(keys)

for keys in ups_member_card.keys():
	every_second_OUT(keys)	

