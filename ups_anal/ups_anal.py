from ups_modul.inout.ups_byt import *
import time
file_name = 'inout_0.4_test.txt'

# time formats
format_time_old = "%W %j %A %d.%m.%Y %H:%M:%S"
format_time_new = "%d.%m.%Y %H:%M:%S"


ups_analytics = {}
for c in range(len(ups_member_card)):
	for key, value in ups_member_card.items():
		ups_analytics[key] = {
			"IN" : 0,
			"IN_count" : 0,
			"OUT" : 0,
			"OUT_count" : 0,
			"ALL" : 0,
			"time" : None,
		}


# script
with open(file_name) as fn:
	for log_row, log_line in enumerate(fn):
		parse_line = log_line.strip().split(" ")
		parse_name = parse_line[0]
		parse_status = parse_line[1]
		time_log = " ".join(parse_line[2:])
		if parse_name in ups_analytics.keys():
			parse_time_raw = time.strptime(time_log, format_time_old)
			time_new_format = time.strftime(format_time_new, parse_time_raw)
			time_seconds = time.mktime(parse_time_raw)
			if ups_analytics[parse_name]["time"] == None:
				ups_analytics[parse_name]["time"] = time_seconds
				continue
			t_delta = time_seconds - ups_analytics[parse_name]["time"]
			if parse_status == "IN":
				ups_analytics[parse_name]["OUT"] += t_delta
				ups_analytics[parse_name]["IN_count"] += 1
			elif parse_status == "OUT":
				ups_analytics[parse_name]["IN"] += t_delta
				ups_analytics[parse_name]["OUT_count"] += 1
			ups_analytics[parse_name]["ALL"] += t_delta
			ups_analytics[parse_name]["time"] = time_seconds
