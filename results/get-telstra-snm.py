import sys
from matplotlib import pyplot as plt

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
stat_file = argument[2]
results = process(result_file)
print(len(results))
sizes = ['0.1', '0.3', '0.5', '0.7', '0.9', '1.1', '1.3', '2', '3']

f = open(stat_file, "w")
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
strategys = ['LCE', 'LCD', 'PROB_CACHE', 'MEDGE', 'CTEDGE']
graph_latency = {}
for strategy in strategys:
	graph[strategy] = []
	for size in sizes:
		for exp in results:
			if exp["strategy"] == strategy and exp["size"] == size:
				graph[strategy].append(exp["latency"])

graph_hit = {}
for strategy in strategys:
	graph[strategy] = []
	for size in sizes:
		for exp in results:
			if exp["strategy"] == strategy and exp["size"] == size:
				graph[strategy].append(exp["hit"])

lce_latency = graph_latency["LCE"]
lcd_latency = graph_latency['LCD']
edge_latency = graph_latency['MEDGE']
coor_latency = graph_latency['CTEDGE']

lce_hit = graph_hit['LCE']
lcd_hit = graph_hit['LCD']
edge_hit = graph_hit['MEDGE']
coor_hit = graph_hit['CTEDGE']

line_up, = plt.plot(size, lru_global, "ro-")
line_down, = plt.plot(size, lru_small, "y.-")
line_upp, = plt.plot(size, lru_filter, "b*-")
plt.xlabel("cache size ")
plt.ylabel("Hit Probability")
plt.legend([line_upp, line_up, line_down], ['Coordinated with filter', 'Coordinated', 'Independent'], bbox_to_anchor=(1, 0.8))
plt.show()
'''

