import os; os.chdir('C:\\Users\\user\\Desktop\\path')
import json
from epidemie_functions import *

f = open('plot_lists.json', 'r')
out = json.load(f)

x_atteinte_list = out[1]
p2list = out[0]

plot_stats(x_atteinte_list, p2list)
