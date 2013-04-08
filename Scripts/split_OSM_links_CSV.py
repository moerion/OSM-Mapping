# This script extracts OSM link information from a .xls file and writes only the links that are roads into a new .xls file.

print 'Splitting links...'
import string
import csv

# format csv link file reader
linkReader = csv.reader(open('OSM_links.csv', 'rb'))

# format csv file writer
f = csv.writer(open("OSM_links_split.csv", "wb"), delimiter=',', lineterminator='\n')

# write column titles
f.writerow(['New Link ID', 'OSM Link ID','Type','Name','Name Type', 'Total Nodes', 'Nodes'])

newLinkId = 1

line = 0

for linkRow in linkReader:
	# skip header
	if (line > 0):
		# parse data
		linkId = linkRow[0]
		linkType = linkRow[1]
		linkName = linkRow[2]
		linkNameType = linkRow[3]
		linkNodesTot = int(linkRow[4])
		linkNodes = linkRow[5:(5+int(linkNodesTot))]
		
		# skip first node in list
		tmpNodesTot = 1
		nodesRead = 1
		
		# node iterator
		i = 0
	
		# iterate through nodes in link
		while (nodesRead < linkNodesTot):
			
			# format csv node file reader
			nodeReader = csv.reader(open('OSM_nodes.csv', 'rb'))
			
			# boolean to keep track of split links
			split = False
			
			# search through node database
			for nodeRow in nodeReader:
				
				nodeId = nodeRow[0]
				nodeProps = nodeRow[3]

				# node found in database
				if (nodeId == linkNodes[nodesRead]):
					
					# node has properties
					if (nodeProps != '0'):
						# split link and write new link to file
						f.writerow([ newLinkId, linkId, linkType,linkName,linkNameType, tmpNodesTot+1] + linkNodes[i:nodesRead+1])
						i = nodesRead
						tmpNodesTot = 0
						newLinkId += 1
						split = True
						
			# update counters
			nodesRead += 1
			tmpNodesTot += 1
		
		
		# make new link out of remaining nodes and write new link to file
		if (split == False):	
			f.writerow([ newLinkId, linkId, linkType,linkName,linkNameType, tmpNodesTot] + linkNodes[i:nodesRead+1])
			newLinkId += 1
		
	line += 1


print 'Done!'
	