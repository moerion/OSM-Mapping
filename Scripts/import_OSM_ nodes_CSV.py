# This script extracts node information from the OSM .xml file and writes it in a .csv file.

print 'Importing nodes...'

import string
import csv

# format csv output file
f = csv.writer(open("OSM_nodes.csv", "wb"), delimiter=',', lineterminator='\n')

# store used column numbers
NodeIdCol = 0
LatCol = 1
LonCol = 2
PropCol = 3

# row counter
row = 0

# node boolean
node = False

# write column titles
f.writerow(['Node ID','Latitude','Longitude','Properties'])

# open file to read
#try:
infile = open('map.xml', 'r')
for line in infile:
	
	if (node == True):
		str = '<tag k="highway" v="'
		strIndex = string.find(line, str)
		
		# Node has properties
		if (strIndex != -1):
			strLen = len(str)
			str = '"/>'
			# write Properties to file
			props = line[strIndex+strLen : string.find(line, str)] # store Node Properties
		
		# write Node information to file
		f.writerow([nodeId,lat,lon,props])
			
	node = False
	
	# clear Node information
	nodeId = 0
	lat = 0
	lon = 0
	props = 0
	
	str = '<node id="'
	strIndex = string.find(line, str)
	
	# new Node entry
	if (strIndex != -1):
		node = True
		row += 1
		strLen = len(str)
		str = '" lat="'
		# write Node IDs to file
		nodeId = line[strIndex+strLen : string.find(line, str)] # store Node ID
		
		strIndex = string.find(line, str)
		if (strIndex != -1):
			strLen = len(str)
			str = '" lon="'
			lat = line[strIndex+strLen : string.find(line, str)] # store Node Latitude
			
			strIndex = string.find(line, str)
			if (strIndex != -1):
				strLen = len(str)
				str = '" user="'
				lon = line[strIndex+strLen : string.find(line, str)] # store Node Longitude
				
#except:
#	print 'Error reading file'
#else:
infile.close()
print 'Done!'
	

		