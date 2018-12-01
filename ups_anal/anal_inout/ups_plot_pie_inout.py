from ups_anal import *
import time
import matplotlib.pyplot as pylot
import matplotlib.gridspec as GridSpec
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Roboto']


def make_autopct(values):
	def my_autopct(pct):
		total = sum(values)
		days = int((pct*total/100.0/60/60/24)+0.5)
		hours = int((pct*total/100.0/60/60))
		return "{h}H [{v:d}D] {p:.0f}%".format(h=hours, v=days, p=pct)
	return my_autopct


def plot(key_name):
	labels_status = ['IN', 'OUT']
	sizes = [ups_analytics["{}".format(key_name)]["IN"], ups_analytics["{}".format(key_name)]["OUT"]]
	colors = ['#FFB025','#09CCCC']
	explode = (0, 0)
	fig0, ax0 = pylot.subplots()
	ax0.pie(sizes, explode=explode, labels=labels_status, autopct=make_autopct(sizes), shadow=False, startangle=90, textprops=None, colors=colors)
	ax0.axis('equal')
	pylot.title("{}".format(key_name), fontweight="bold")
	pylot.savefig("{}_pie.png".format(key_name), dpi=300)


for key in ups_analytics.keys():
	plot(key)