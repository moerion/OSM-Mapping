# This script extracts lane information from a DynusT .xls file and adds it to the OSM links .csv file.

print 'Splitting links...'

# xlrd library found at (http://pypi.python.org/pypi/xlrd)
import xlrd
import string
import csv

# open workbooks
wb_Dyn_nodes = xlrd.open_workbook('DynusT_nodes.xls')
wb_Dyn_links = xlrd.open_workbook('Node and Link Properties.xls')

# load sheets
sh_Dyn_nodes = wb_Dyn_nodes.sheet_by_index(0)
sh_Dyn_links = wb_Dyn_links.sheet_by_index(1)


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
		linkNodesTot = int(linkRow[6])
		linkNodes = linkRow[7:(7+int(linkNodesTot))]
		linkLanes = 0
	
		for DynLinkRow in range(sh_Dyn_links.nrows):
			# skip header
			if (DynLinkRow > 0):
				nodeAId = sh_Dyn_links.cell(DynLinkRow, 1).value
				nodeBId = sh_Dyn_links.cell(DynLinkRow, 2).value
				
				# get lat and lon for Dyn nodes
				for DynNodeRow in range(sh_Dyn_nodes.nrows):
					
					DynNodeId = sh_Dyn_nodes.cell(DynNodeRow, 0).value
					print DynNodeId
					if (nodeAId == DynNodeId):
						NodeALat = float(sh_Dyn_nodes.cell(DynNodeRow, 2).value)
						NodeALon = float(sh_Dyn_nodes.cell(DynNodeRow, 1).value)
						
					elif (nodeBId == DynNodeId):
						NodeBLat = float(sh_Dyn_nodes.cell(DynNodeRow, 2).value)
						NodeBLon = float(sh_Dyn_nodes.cell(DynNodeRow, 1).value)
			
			nodeAFound = False
			nodeBFound = False
			nodesFound = False
			
			nodesRead = 0
			
			# iterate through nodes in link
			while ((nodesRead < linkNodesTot)&(nodesFound == False)):
				
				# format csv node file reader
				nodeReader = csv.reader(open('OSM_nodes.csv', 'rb'))
				
				nodeLine = 0
				# search through node database
				for nodeRow in nodeReader:
					if (nodeLine == 0):
						nodeLine += 1
					else:
						nodeId = nodeRow[0]
						nodeLat = float(nodeRow[1])
						nodeLon = float(nodeRow[2])
						
						# link node found in database
						if (linkNodes[nodesRead] == nodeId):
							# link node lat matches Dyn node lat
							if ((nodeALat >= (nodeLat - .0001))&(nodeALat <= (nodeLat + .0001))):
								# link node lon matches Dyn node lon
								if ((nodeALon >= (nodeLon - .0001))&(nodeALon <= (nodeLon + .0001))):
									nodeAFound = True
							# link node lat matches Dyn node lat
							elif ((nodeBLat >= (nodeLat - .0001))&(nodeBLat <= (nodeLat + .0001))):
								# link node lon matches Dyn node lon
								if ((nodeBLon >= (nodeLon - .0001))&(nodeBLon <= (nodeLon + .0001))):
									nodeBFound = True
							
							if ((nodeAFound == True)&(nodeBFound == True)):
								nodesFound = True
							
				# update counter
				nodesRead += 1
			
			if (nodesFound == True):
				linkLanes = linkLanes + int(sh_Dyn_links.cell(DynLinkRow, 6).value)
		
		if (linkLanes == 0):
			linkLanes = 4
		
		# write new link information to file
		f.writerow([ linkId, linkOSMId, linkType,linkName,linkNameType, linkLanes, tmpNodesTot] + linkNodes)
		
	line += 1


print 'Done!'
	