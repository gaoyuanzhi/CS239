import json
import collections
import datetime
import matplotlib.pyplot as plt
import calendar
import numpy as np
import math
from scipy.stats import pearsonr, spearmanr


def add_months(sourcedate,months):
	month = sourcedate.month - 1 + months
	year = int(sourcedate.year + month / 12 )
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.datetime(year,month,day,0)

def generatePopularityChagneGraph(id):
	f = open('../../data2/'+str(id)+'.json', "r")
	jsonData = (f.readlines())[0]
	f.close()

	f = open('../../data2_2/'+str(id)+'.json', "r")
	jsonData2 = (f.readlines())[0]
	f.close()

	data = json.loads(jsonData)
	data2 = json.loads(jsonData2)

	projectName = data.keys()[0]
	projectValue = data.values()[0]
	projectValue2 = data2.values()[0]


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


	# order the star data
	xy0 = {}
	for key, value in projectValue[0].items():
		xy0.update({datetime.datetime.strptime(key, '%Y-%m'):value})
	xy0 = collections.OrderedDict(sorted(xy0.items()))
	stars = sum(xy0.values())


	flagTime = changes.keys()[0]
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
	forks = sum(xy1.values())

	flagTime = changes.keys()[0]
	while flagTime < datetime.datetime.now():
		if flagTime in xy1.keys():
			pass
		else:
			xy1.update({flagTime: 0})
		flagTime = add_months(flagTime,1)
	xy1 = collections.OrderedDict(sorted(xy1.items()))


	# order pull data
	xy2 = {}
	for key, value in projectValue[3].items():
		xy2.update({datetime.datetime.strptime(key, '%Y-%m'):pow(value,2)})

	xy2 = collections.OrderedDict(sorted(xy2.items()))

	flagTime = changes.keys()[0]
	while flagTime < datetime.datetime.now():
		if flagTime in xy2.keys():
			pass
		else:
			xy2.update({flagTime: 0})
		flagTime = add_months(flagTime,1)
	xy2 = collections.OrderedDict(sorted(xy2.items()))
	pulls = sum(xy2.values())

	# issue data
	xy3 = {}
	for key, value in projectValue[4].items():
		xy3.update({datetime.datetime.strptime(key, '%Y-%m'):pow(value,2)})

	xy3 = collections.OrderedDict(sorted(xy3.items()))

	flagTime = changes.keys()[0]
	while flagTime < datetime.datetime.now():
		if flagTime in xy3.keys():
			pass
		else:
			xy3.update({flagTime: 0})
		flagTime = add_months(flagTime,1)
	xy3 = collections.OrderedDict(sorted(xy3.items()))
	issues = sum(xy3.values())

	basicInfo = {"star":stars, "fork":forks, "pull":pulls, "issue":issues}


	# readme change
	xy4 = {}
	for key, value in projectValue2[0].items():
		xy4.update({datetime.datetime.strptime(key, '%Y-%m'):value})

	xy4 = collections.OrderedDict(sorted(xy4.items()))

	flagTime = changes.keys()[0]
	while flagTime < datetime.datetime.now():
		if flagTime in xy4.keys():
			pass
		else:
			xy4.update({flagTime: 0})
		flagTime = add_months(flagTime,1)
	xy4 = collections.OrderedDict(sorted(xy4.items()))



	# # method 1 readme / stars
	# popularity = dict(collections.Counter(xy0))
	# changes = xy4;

	# # method 2
	# popularity = dict(collections.Counter(xy0)+collections.Counter(xy1)+collections.Counter(xy2))

	# method 3
	popularity = dict(collections.Counter(xy0)+collections.Counter(xy1)+collections.Counter(xy2)+collections.Counter(xy3))
	popularity = collections.OrderedDict(sorted(popularity.items()))


	listOfChange = []
	listOfPop = []

	output = []
	for key,value in changes.items():
		if key in popularity.keys():
			output.append([key,popularity[key],value])
			listOfChange.append(value)
			listOfPop.append(popularity[key])
		else:
			output.append([key,0,value])
			listOfChange.append(value)
			listOfPop.append(0)

	print str(np.mean(listOfChange)) + "\t" + str(np.mean(listOfPop)) +"\t" + str(pearsonr(listOfChange,listOfPop)[0]) + "\t"+ str(spearmanr(listOfChange,listOfPop)[0])

	person = round(pearsonr(listOfChange,listOfPop)[0],4)
	spearman = round(spearmanr(listOfChange,listOfPop)[0],4)
	correlation = {"person":person, "spearman": spearman}

	# with plt.xkcd():
	fig, ax = plt.subplots()
	# ax.plot(xy0.keys(),xy0.values(),'k--', label='stars')
	# ax.plot(xy1.keys(),xy1.values(),'k:', label='forks')
	# ax.plot(xy2.keys(),xy2.values(),'k', label='pulls')
	ax.plot(popularity.keys(),popularity.values(),'k',color = 'green',label='popularity')
	# ax.set_xlabel('Time')
	legend = ax.legend(loc='upper left', shadow=False,  fontsize='small')

	ax2 = ax.twinx()
	ax2.set_ylabel('change', color='blue')
	ax2.tick_params('y', colors='blue')
	ax2.plot(changes.keys(),changes.values(),'k',color='blue',label='change')

	# legend.get_frame().set_facecolor('#00FFCF')

	web = json.dumps({"basicInfo":basicInfo,"correlation":correlation})
	# print web
	name = projectName[-4:]
	f = open("../../web/"+name+".json",'wr')
	f.write(web)
	f.close()

	# beautify the x-labels
	plt.gcf().autofmt_xdate()
	# plt.axes().set_aspect(1)
	# plt.show()
	f = open("../../web/"+name+".tsv",'wr')
	f.write("date\tpupularity\tchange")
	for x in output:
		f.write("\n{}\t{}\t{}".format(x[0].strftime("%Y%m%d"),x[1],x[2]))
	plt.savefig("../../data2/fig/" + str(id)+".pdf")

	f.close()
	
if __name__ == '__main__':
	for x in range(1,11):
		generatePopularityChagneGraph(x)
	# generatePopularityChagneGraph(2)
