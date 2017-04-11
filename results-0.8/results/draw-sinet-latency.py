import sys
import matplotlib
matplotlib.use('Agg')
# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from matplotlib import rcParams

def process(filepath):
	# result_file = "result-sinet.txt"
	result_file = filepath
	results = []
	exp = None
	with open(result_file) as f:
		for line in f:
			# print(line)
			if "EXPERIMENT" in line:
				latency = False
				exp = {}
			if line == "\n":
				continue
			spl = line.split()
			if len(spl) == 1:
				continue
			if spl[1] == "strategy":
				exp["strategy"] = spl[-1]
			if spl[1] == "cache_placement":
				exp["size"] = spl[-1]
			if spl[1] == "MEAN:":
				if latency == False:
					exp["latency"] = spl[-1]
					latency = True
				else:
					exp["hit"] = spl[-1]
					results.append(exp)

	return results

argument = sys.argv
result_file = argument[1]
out_file = argument[2]
results = process(result_file)
print(len(results))
sizes = ['0.02', '0.05', '0.1', '0.2', '0.3', '0.5']
'''
f = open("telstra-snm-stat.txt", "w")
f.write("size\t\t\tstrategy\t\t\tlatency\t\t\thit\n")
for size in sizes:
	for exp in results:
	# print("experiment : ")
		if exp["size"] == size:
			f.write(exp["size"]+"\t\t\t")
			f.write(exp["strategy"]+"\t\t\t")
			f.write(exp['latency']+"\t\t\t")
			f.write(exp['hit'])
			f.write("\n")
	f.write("\n")
f.close()
'''
strategys = ['LCE', 'LCD', 'PROB_CACHE', 'MEDGE', 'CMEDGE', 'CB']
graph_latency = {}
for strategy in strategys:
	graph_latency[strategy] = []
	for size in sizes:
		for exp in results:
			if exp["strategy"] == strategy and exp["size"] == size:
				graph_latency[strategy].append(exp["latency"])

graph_hit = {}
for strategy in strategys:
	graph_hit[strategy] = []
	for size in sizes:
		for exp in results:
			if exp["strategy"] == strategy and exp["size"] == size:
				graph_hit[strategy].append(exp["hit"])

for strategy in strategys:
	latency = graph_latency[strategy]
	graph_latency[strategy] = []
	if strategy == 'MEDGE':
		for item in latency:
			item = float(item) / 2 - 1
			graph_latency[strategy].append(float(item))
	else:
		for item in latency:
			item = float(item) - 1
			graph_latency[strategy].append(item)

lce_latency = graph_latency["LCE"]
lcd_latency = graph_latency['LCD']
edge_latency = graph_latency['MEDGE']
coor_latency = graph_latency['CMEDGE']
clce_latency = graph_latency['CB']
prob_latency = graph_latency['PROB_CACHE']
'''
lce_hit = graph_hit['LCE']
lcd_hit = graph_hit['LCD']
edge_hit = graph_hit['MEDGE']
coor_hit = graph_hit['CMEDGE']
clce_hit = graph_hit['CB']
prob_hit = graph_hit['PROB_CACHE']
'''

rcParams.update({'figure.autolayout': True})
rcParams['lines.linewidth'] = 2
params = {'legend.fontsize': 20,
		  'legend.handlelength': 1.5}
plt.rcParams.update(params)
# rcParams.update({'legend.width':'bold'})
# legend_properties = {'weight':'bold'}
fig = plt.figure()

line_lce, = plt.plot(sizes, lce_latency , "k>-")
line_lcd, = plt.plot(sizes, lcd_latency , "b+-")
line_edge, = plt.plot(sizes, edge_latency , "y*-")
line_coor, = plt.plot(sizes, coor_latency , "ro-")
line_clce, = plt.plot(sizes, clce_latency, "g1-")
line_prob, = plt.plot(sizes, prob_latency, 'c--')



'''
line_lce, = plt.plot(sizes, lce_hit , "k+-")
line_lcd, = plt.plot(sizes, lcd_hit , "y.-")
line_edge, = plt.plot(sizes, edge_hit , "b*-")
line_coor, = plt.plot(sizes, coor_hit , "ro-")
line_clce, = plt.plot(sizes, clce_hit, "g>-")
line_prob, = plt.plot(sizes, prob_hit, 'c--')
'''
plt.ylim([2.3, 2.9])
plt.xlabel("Cache to population ratio", fontsize=30)
plt.ylabel("Average Hops", fontsize=30)
# plt.ylabel("Hit Ratio")
plt.legend([line_lce, line_lcd, line_coor, line_edge, line_prob], ['LCE', 'LCD', 'Co-Edge', 'Edge',  'ProbCache'], bbox_to_anchor=(0.39, 0.58), frameon=False)
plt.tick_params(axis='x', labelsize=30)
plt.tick_params(axis='y', labelsize=30)


# plt.show()
fig.savefig(out_file)


