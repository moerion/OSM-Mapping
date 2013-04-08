# This script extracts lane information from a DynusT .xls file and adds it to the OSM links .csv file.

print 'Splitting links...'


import string
import csv

# format csv link file reader
linkReader = csv.reader(open('OSM_links_split.csv', 'rb'))

# format csv file writer
f = csv.writer(open("OSM_links_final.csv", "wb"), delimiter=',', lineterminator='\n')

# write column titles
f.writerow(['New Link ID', 'OSM Link ID','Type','Name','Name Type', 'Lanes', 'Total Nodes', 'Nodes'])

newLinkId = 1

line = 0

for linkRow in linkReader:
	# skip header
	if (line > 0):
		# parse data
		linkId = linkRow[0]
		linkOSMId = linkRow[1]
		linkType = linkRow[2]
		linkName = linkRow[3]
		linkNameType = linkRow[4]
		linkNodesTot = int(linkRow[5])
		linkNodes = linkRow[6:(6+int(linkNodesTot))]
		linkLanes = 4
		
		# write new link information to file
		f.writerow([ linkId, linkOSMId, linkType,linkName,linkNameType, linkLanes, linkNodesTot] + linkNodes)
		
	line += 1


print 'Done!'
	