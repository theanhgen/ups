import time
import numpy as np
import matplotlib
import matplotlib.pyplot as pylot
from ups_modul.inout.ups_byt import *
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Roboto']

file_name = 'inout_0.4_IN.txt'


# time formats
format_time_old = "%W %j %A %d.%m.%Y %H:%M:%S"
format_time_new = "%d.%m.%Y %H:%M:%S"


ups_data = {}
for c in range(len(ups_member_card)):
	for key, value in ups_member_card.items():
		ups_data[key] = {
			"inout_log" : [],
			"weekday" : [0 for x in range(24)],
				}


with open(file_name) as fn:
	for log_row, log_line in enumerate(fn):
		parse_line = log_line.strip().split(" ")
		parse_name = parse_line[0]
		parse_status = parse_line[1]
		parse_day = parse_line[4]
		parse_time_stamp = parse_line[6].strip().split(":")
		parse_hour = parse_time_stamp[0]
		time_log = " ".join(parse_line[2:])
		if parse_name in ups_data.keys():
			parse_time_raw = time.strptime(time_log, format_time_old)
			time_new_format = time.strftime(format_time_new, parse_time_raw)
			time_seconds = time.mktime(parse_time_raw)
			time_log_status = "{} {}".format(parse_status, time_new_format)
			ups_data[parse_name]["inout_log"].append(time_log_status)
			if parse_status == "IN":
				ups_data[parse_name]["weekday"][int(parse_hour)] += 1


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    if not ax:
        ax = pylot.gca()
    im = ax.imshow(data, **kwargs)
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw, fraction=0.0155, pad=0.03)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom", fontweight="regular", fontsize=20)
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_xticklabels(col_labels, fontweight="regular", fontsize=16)
    ax.set_yticklabels(row_labels, fontweight="regular", fontsize=16)
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)
    pylot.setp(ax.get_xticklabels(), rotation=0, ha="center",
             rotation_mode="anchor")
    for edge, spine in ax.spines.items():
        spine.set_visible(False)
    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    # ax.grid(which="minor", color="w", linestyle='-', linewidth=2.5)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{:.0f}",
                     textcolors=["white", "black"],
                     threshold=None, **textkw):
    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)
    texts = []
    # for i in range(data.shape[0]):
    #     for j in range(data.shape[1]):
    #         kw.update(color=textcolors[im.norm(data[i, j]) > threshold])
    #         text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
    #         texts.append(text)
    # return texts


members = ["Andrej", "Roman", "Sasha", "Lina",
              "Tung", "Chuot", "Marie", "Linh", "Tu", "Rudolf"]
hours = [x for x in range(24)]


def plot():
    ups_in = np.array([ups_data["{}".format("Andrej")]["weekday"],
                    ups_data["{}".format("Roman")]["weekday"],
                    ups_data["{}".format("Sasha")]["weekday"],
                    ups_data["{}".format("Lina")]["weekday"],
                    ups_data["{}".format("Tung")]["weekday"],
                    ups_data["{}".format("Chuot")]["weekday"],
                    ups_data["{}".format("Marie")]["weekday"],
                    ups_data["{}".format("Linh")]["weekday"]])
    fig, ax = pylot.subplots(figsize=(12,4))
    im, cbar = heatmap(ups_in, members, hours, ax=ax,
                   cmap="inferno", cbarlabel="{}: {}".format("IN in the day", "UPS CORP"))
    texts = annotate_heatmap(im, valfmt="{x:.0f}", fontsize=13)
    pylot.savefig("{}_IN_heatmap.png".format("UPS_CORP"), dpi=500)


plot()

