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

names = ["Andrej", "Roman", "Sasha", "Lina", "Tung", "Chuot", "Marie", "Linh", "Tu", "Rudolf"]

means_IN = []
for name in names:
	means_IN.append((ups_analytics[name]['IN_count']))

# std_men = (0, 0, 0, 0, 0, 0, 0, 0)


means_OUT = []
for name in names:
	means_OUT.append((ups_analytics[name]['OUT_count']))

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
ax.set_ylabel("in/out count")
ax.set_title('UPS CORP', fontweight="bold")
ax.set_xticks(index + bar_width / 2)
# for name in names:
ax.set_xticklabels(names)
ax.legend()


def autolabel(rects, xpos='center'):
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')


autolabel(rects1, "left")
autolabel(rects2, "right")

pylot.savefig("{}.png".format("UPS CORP_count"), dpi=200)
fig.tight_layout
