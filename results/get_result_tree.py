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
			if spl[1] == "desc":
				exp["branch"] = spl[7].rstrip(',')
				exp["strategy"] = spl[9].rstrip(',')
				exp["topology"] = spl[11].rstrip(',')
				exp["size"] = spl[14]
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
branch = ['2', '3', '4', '5']
sizes = ['1', '5', '10']


f = open("result_cluster.txt", "w")
f.write("branching-factor\t\t\tsize\t\t\tstrategy\t\t\tlatency\t\t\thit\n")
for br in branch:
	for size in sizes:
		for exp in results:
	# print("experiment : ")
			if exp["branch"] == br and exp["size"] == size:
				f.write(exp["branch"]+"\t\t\t")
				f.write(exp["size"]+"\t\t\t")
				f.write(exp["strategy"]+"\t\t\t")
				f.write(exp['latency']+"\t\t\t")
				f.write(exp['hit'])
				f.write("\n")
		f.write("\n")
	f.write("\n\n")
	# print(exp["strategy"])
	# print(exp["size"]) 
	# print(exp["latency"])
	# print(exp["hit"])
	# print("\n")
f.close()
