import csv
import sys

infile = sys.argv[1]
TOPICS = 50
id_topic = {}
with open(infile, 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter="\t")
	for row in csvreader:
		postid = row[1]
		id_topic[postid] = {}
		for x in range(0,TOPICS-1):
			id_topic[postid][float(row[x+2])] = x

	for i in id_topic.keys():
		print("%s\t%s" % (i, id_topic[i][sorted(id_topic[i].keys(), reverse=True)[0]]))
