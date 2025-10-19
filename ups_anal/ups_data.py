from ups_modul.inout.ups_byt import *
import time
file_name = 'inout_0.4_test.txt'


# time formats
format_time_old = "%W %j %A %d.%m.%Y %H:%M:%S"
format_time_new = "%d.%m.%Y %H:%M:%S"


ups_data = {}
for c in range(len(ups_member_card)):
	for key, value in ups_member_card.items():
		ups_data[key] = {
			"inout_log" : [],
			}


with open(file_name) as fn:
	for log_row, log_line in enumerate(fn):
		parse_line = log_line.strip().split(" ")
		parse_name = parse_line[0]
		parse_status = parse_line[1]
		time_log = " ".join(parse_line[2:])
		if parse_name in ups_data.keys():
			parse_time_raw = time.strptime(time_log, format_time_old)
			time_new_format = time.strftime(format_time_new, parse_time_raw)
			time_seconds = time.mktime(parse_time_raw)
			time_log_status = "{} {}".format(parse_status, time_new_format)
			ups_data[parse_name]["inout_log"].append(time_log_status)
			