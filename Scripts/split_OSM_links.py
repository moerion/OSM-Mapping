# This script extracts OSM link information from a .xls file and writes only the links that are roads into a new .xls file.

print 'Splitting links...'

# xlrd library found at (http://pypi.python.org/pypi/xlrd)
import xlrd

# xlwt library found at (http://pypi.python.org/pypi/xlwt)
import xlwt

# open workbooks
wb_links = xlrd.open_workbook('OSM_links_clean.xls')
wb_nodes = xlrd.open_workbook('OSM_nodes.xls')

# load sheets
sh_links = wb_links.sheet_by_index(0)
sh_nodes = wb_nodes.sheet_by_index(0)

# format xls output file
w = xlwt.Workbook()
ws = w.add_sheet('Links')

# store used column numbers
NewLinkIdCol = 0
OSMLinkIdCol = 1
LanesCol = 2
TypeCol = 3
NameCol = 4
NameTypeCol = 5
NodesTotCol = 6
NodesCol = 7

readLinkIdCol = 0
readLanesCol = 1
readTypeCol = 2
readNameCol = 3
readNameTypeCol = 4
readNodesTotCol = 5
readNodesCol = 6

readNodeIdCol = 0
readPropCol = 3

# row counter
row = 0

# Node ID
nodeId = 0

# node counters
oldNodesTot = 0
newNodesTot = 0
nodesRead = 0
tmpNodesRead = 0
nodes = 0

# Link IDs
newLinkId = 1
OSMLinkId = 0

# split Link boolean
split = False

# write column titles
ws.write(row, NewLinkIdCol, 'Link ID')
ws.write(row, OSMLinkIdCol, 'OSM ID')
ws.write(row, LanesCol, 'Lanes')
ws.write(row, TypeCol, 'Type')
ws.write(row, NameCol, 'Name')
ws.write(row, NameTypeCol, 'Name Type')
ws.write(row, NodesTotCol, 'Total Nodes')
ws.write(row, NodesCol, 'Nodes')

# skip a row
row += 2

for rownum in range(sh_links.nrows):
    	
	if (rownum > 1):
		
		OSMLinkId = sh_links.cell(rownum, readLinkIdCol).value
		ws.write(row, NewLinkIdCol, newLinkId)
		ws.write(row, OSMLinkIdCol, OSMLinkId)
		ws.write(row, LanesCol, sh_links.cell(rownum, readLanesCol).value)
		ws.write(row, TypeCol, sh_links.cell(rownum, readTypeCol).value)
		ws.write(row, NameCol, sh_links.cell(rownum, readNameCol).value)
		ws.write(row, NameTypeCol, sh_links.cell(rownum, readNameTypeCol).value)
		
		# copy Nodes
		oldNodesTot = sh_links.cell(rownum, readNodesTotCol).value
		newNodesTot = 0
		nodesRead = 0
		tmpNodesRead = 0
		nodes = 0
		
		while (nodesRead < oldNodesTot):
			if (tmpNodesRead == 250):
				rownum += 1
				tmpNodesRead = 0
				
			nodeId = sh_links.cell(rownum, readNodesCol+tmpNodesRead).value
			
			if (nodes == 250):
				row += 1
				nodes = 0
				
			ws.write(row, NodesCol+nodes, nodeId)
			
			for rownum1 in range(sh_nodes.nrows):
				if (nodeId == sh_nodes.cell(rownum1, readNodeIdCol).value):
					if (sh_nodes.cell(rownum1, readPropCol).value != ''):
						split = True
			
			newNodesTot += 1
						
			if (split == True):
				split = False
				ws.write(row, NodesTotCol, newNodesTot)
				# new row
				row += 1
				newLinkId += 1
				nodes = 0
				ws.write(row, NewLinkIdCol, newLinkId)
				ws.write(row, OSMLinkIdCol, OSMLinkId)
				ws.write(row, LanesCol, sh_links.cell(rownum, readLanesCol).value)
				ws.write(row, TypeCol, sh_links.cell(rownum, readTypeCol).value)
				ws.write(row, NameCol, sh_links.cell(rownum, readNameCol).value)
				ws.write(row, NameTypeCol, sh_links.cell(rownum, readNameTypeCol).value)
				ws.write(row, NodesCol+nodes, nodeId)
				newNodesTot = 1
				
			nodes += 1
			nodesRead += 1
			tmpNodesRead += 1
		
		if (split == False):
			ws.write(row, NodesTotCol, newNodesTot)
			
		# increment row	
		row +=1
		newLinkId += 1

print 'Done!'
	
w.save('OSM_links_split.xls')