import sys

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
results = process(result_file)
print(len(results))
sizes = ['0.1', '0.3', '0.5', '0.7', '0.9', '1.1', '1.3', '2', '3']

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
