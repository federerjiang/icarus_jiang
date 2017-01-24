import os, sys

def distribute_requests(filename, numberOfRequesters):
	if numberOfRequesters > 1:
		filePath = os.getcwd()
		f = open(filePath + "/" + filename, 'r')
		dictOfDistributedRequested = {}
		i = 0
		while i < numberOfRequesters:
			dictOfDistributedRequested[i] = []
			i = i + 1
		lineNo = 1
		for line in f:
			dictOfDistributedRequested[lineNo % numberOfRequesters].append(line)
			lineNo = lineNo + 1
		for trace in dictOfDistributedRequested:
			fwrite = open(filePath + "/" + filename + "." + str(trace) + ".txt", 'w')
			for item in dictOfDistributedRequested[trace]:
				fwrite.write(item)
			fwrite.close()
			
argumentlist = sys.argv
filename = str(argumentlist[1])
numberOfRequesters = int(argumentlist[2])
distribute_requests(filename, numberOfRequesters)