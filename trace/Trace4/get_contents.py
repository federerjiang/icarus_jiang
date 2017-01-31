from sets import Set
import os

def get_contents(path):
 	os.getcwd()
  	filePath =  os.getcwd() + "/" + path
  	pathRead = filePath
  	pathWrite = os.getcwd() + "/" + "contents.txt"

  	f = open(pathRead, "r")
  	fwrite = open(pathWrite, "w")

  	items = Set()
  	for line in open(pathRead, "r"):
  		items.add(line)

  	for item in items:
  		fwrite.write(item)
  	fwrite.close()

# argument = sys.argv
# path = argument[1]
path = "SNMtrace.txt"
print "Processing trace: ", path
get_contents(path)


