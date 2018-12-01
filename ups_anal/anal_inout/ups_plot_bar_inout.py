from ups_anal import *
import time
import numpy as np
import matplotlib.pyplot as pylot
import matplotlib.gridspec as GridSpec
from matplotlib import rcParams
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Roboto']


n_groups = 9

def hours(seconds):
	hours = seconds/3600
	return hours

names = ["Andrej", "Roman", "Sasha", "Lina", "Tung", "Chuot", "Marie", "Linh", "Tu", "Rudolf"]

means_IN = []
for name in names:
	means_IN.append((hours(ups_analytics[name]['IN'])))

# std_men = (0, 0, 0, 0, 0, 0, 0, 0)


means_OUT = []
for name in names:
	means_OUT.append((hours(ups_analytics[name]['OUT'])))

# std_women = (0, 0, 0, 0, 0, 0, 0, 0)

fig, ax = pylot.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 1
error_config = {'ecolor': '0.3'}
colors = ['#FFB025','#09CCCC']

# yerr=std_men
rects1 = ax.bar(index, means_IN, bar_width,
                alpha=opacity, color='#FFB025',
                error_kw=error_config,
                label='IN')

# yerr=std_women,
rects2 = ax.bar(index + bar_width, means_OUT, bar_width,
                alpha=opacity, color='#09CCCC',
                error_kw=error_config,
                label='OUT')

# ax.set_xlabel('UPS CORP')
ax.set_ylabel('Hours')
ax.set_title('UPS CORP', fontweight="bold")
ax.set_xticks(index + bar_width / 2)
# for name in names:
ax.set_xticklabels(names)
ax.legend()


pylot.savefig("{}.png".format("UPS CORP"), dpi=200)


fig.tight_layout()
# pylot.show()
