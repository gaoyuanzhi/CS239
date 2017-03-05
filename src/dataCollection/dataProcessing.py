import json
import collections
import datetime
import matplotlib.pyplot as plt
import calendar
import numpy as np
import math

def add_months(sourcedate,months):
	month = sourcedate.month - 1 + months
	year = int(sourcedate.year + month / 12 )
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.datetime(year,month,day,0)

def generatePopularityChagneGraph(id):
	f = open('../../data/'+str(id)+'.json', "r")
	jsonData = (f.readlines())[0]
	data = json.loads(jsonData)
	projectName = data.keys()[0]
	projectValue = data.values()[0]

	# order the star data
	xy0 = {}
	for key, value in projectValue[0].items():
		xy0.update({datetime.datetime.strptime(key, '%Y-%m'):value})
	xy0 = collections.OrderedDict(sorted(xy0.items()))

	flagTime = xy0.keys()[0]
	while flagTime < datetime.datetime.now():
		if flagTime in xy0.keys():
			pass
		else:
			xy0.update({flagTime: 0})
		flagTime = add_months(flagTime,1)
	xy0 = collections.OrderedDict(sorted(xy0.items()))

	# order fork data
	xy1 = {}
	for key, value in projectValue[1].items():
		xy1.update({datetime.datetime.strptime(key, '%Y-%m'):value})

	xy1 = collections.OrderedDict(sorted(xy1.items()))

	flagTime = xy1.keys()[0]
	while flagTime < datetime.datetime.now():
		if flagTime in xy1.keys():
			pass
		else:
			xy1.update({flagTime: 0})
		flagTime = add_months(flagTime,1)
	xy1 = collections.OrderedDict(sorted(xy1.items()))

	popularity = dict((collections.Counter(xy0)+collections.Counter(xy1)))
	popularity = collections.OrderedDict(sorted(popularity.items()))


	# calculate changes

	changes = {}
	for key, value in projectValue[2].items():
		change = value[0] * math.log((value[1] + value[2] + 1),100) 
		changes.update({datetime.datetime.strptime(key, '%Y-%m'):change})
	
	changes = collections.OrderedDict(sorted(changes.items()))
	flagTime = changes.keys()[0]
	while flagTime < datetime.datetime.now():
		if flagTime in changes.keys():
			pass
		else:
			changes.update({flagTime: 0})
		flagTime = add_months(flagTime,1)

	changes = collections.OrderedDict(sorted(changes.items()))

# with plt.xkcd():
	fig, ax = plt.subplots()
	ax.plot(xy0.keys(),xy0.values(),'k--', label='stars')
	ax.plot(xy1.keys(),xy1.values(),'k:', label='forks')
	ax.plot(popularity.keys(),popularity.values(),'k',color = 'green',label='popularity')
	# ax.set_xlabel('Time')
	legend = ax.legend(loc='upper left', shadow=False,  fontsize='small')

	ax2 = ax.twinx()
	ax2.set_ylabel('change', color='blue')
	ax2.tick_params('y', colors='blue')
	ax2.plot(changes.keys(),changes.values(),'k',color='blue',label='change')

	# legend.get_frame().set_facecolor('#00FFCF')

	# beautify the x-labels
	plt.gcf().autofmt_xdate()
	# plt.axes().set_aspect(1)
	# plt.show()

	plt.savefig("../../data/fig/" + str(id)+".pdf")

if __name__ == '__main__':
	for x in xrange(1,10):
		generatePopularityChagneGraph(x)
