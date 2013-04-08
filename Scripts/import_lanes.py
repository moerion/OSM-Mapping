# This script extracts lane information from a DynusT .xls file and adds it to the OSM links .xls file.

# xlrd library found at (http://pypi.python.org/pypi/xlrd)
import xlrd

# xlwt library found at (http://pypi.python.org/pypi/xlwt)
import xlwt

# open workbooks
wb_OSM_links = xlrd.open_workbook('OSM_links_split.xls')
wb_OSM_nodes = xlrd.open_workbook('OSM_nodes.xls')
wb_Dyn_nodes = xlrd.open_workbook('DynusT_nodes.xls')
wb_Dyn_links = xlrd.open_workbook('Node and Link Properties.xls')

# load sheets
sh_OSM_links = wb_OSM_links.sheet_by_index(0)
sh_OSM_nodes = wb_OSM_nodes.sheet_by_index(0)
sh_Dyn_nodes = wb_Dyn_nodes.sheet_by_index(0)
sh_Dyn_links = wb_Dyn_links.sheet_by_index(1)

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

NodeIdCol = 0
OSMLatCol = 1
OSMLonCol = 2

DynLonCol = 1
DynLatCol = 2

NodeACol = 1
NodeBCol = 2
DynLanesCol = 6

# node counter
nodesTot = 0
nodesRead = 0

# node variables
OSMNodeA = 0
OSMNodeALat = 0
OSMNodeALon = 0
OSMNodeB = 0
OSMNodeBLat = 0
OSMNodeBLon = 0
DynNodeA = 0
DynNodeALat = 0
DynNodeALon = 0
DynNodeB = 0
DynNodeBLat = 0
DynNodeBLon = 0

# temp variables
tempLat = 0
tempLon = 0
tempNodeId = 0
tempLanes = 0
tempNodesRead = 0

#
## functions:
#

# get coordinates for OSM node
def get_OSM_coords( node ):
	
	tempLat = 0
	tempLon = 0
	
	# match Node ID
	for rownum1 in range(sh_OSM_nodes.nrows):
		if (node == sh_OSM_nodes.cell(rownum1, NodeIdCol).value):
			tempLat = sh_OSM_nodes.cell(rownum1, OSMLatCol).value
			tempLon = sh_OSM_nodes.cell(rownum1, OSMLonCol).value
			rownum1 = 0
			break

# match OSM node to DynusT node
def match_nodes( lat, lon ):

	tempNodeId = 0
	
	# match coordinates
	for rownum1 in range(sh_Dyn_nodes.nrows):
		if (rownum1 > 1):
			if (((lat >= sh_Dyn_nodes.cell(rownum1, DynLatCol).value - 0.0001)) | (lat <= sh_Dyn_nodes.cell(rownum1, DynLatCol).value + 0.0001)):
				if ((lon >= (sh_Dyn_nodes.cell(rownum1, DynLonCol).value - 0.0001)) | (lon <= (sh_Dyn_nodes.cell(rownum1, DynLonCol).value + 0.0001))):
					tempNodeId = sh_Dyn_nodes.cell(rownum1, NodeIdCol).value
					rownum1 = 0
					break
			
# get lane information
def get_lanes( nodeA, nodeB ):
	
	for rownum1 in range(sh_Dyn_links.nrows):
		if (nodeA == sh_Dyn_links.cell(rownum1, NodeACol).value):
			if (nodeB == sh_Dyn_links.cell(rownum1, NodeBCol).value):
				tempLanes += sh_Dyn_links.cell(rownum1, DynLanesCol).value
				rownum1 = 0
				break
	
#
## main:
#

# write column titles
ws.write(0, NewLinkIdCol, 'Link ID')
ws.write(0, OSMLinkIdCol, 'OSM ID')
ws.write(0, LanesCol, 'Lanes')
ws.write(0, TypeCol, 'Type')
ws.write(0, NameCol, 'Name')
ws.write(0, NameTypeCol, 'Name Type')
ws.write(0, NodesTotCol, 'Total Nodes')
ws.write(0, NodesCol, 'Nodes')


for rownum in range(sh_OSM_links.nrows):
	if (rownum > 1):
		# copy available information
		ws.write(rownum, NewLinkIdCol, sh_OSM_links.cell(rownum, NewLinkIdCol).value)
		ws.write(rownum, OSMLinkIdCol, sh_OSM_links.cell(rownum, OSMLinkIdCol).value)
		ws.write(rownum, TypeCol, sh_OSM_links.cell(rownum, TypeCol).value)
		ws.write(rownum, NameCol, sh_OSM_links.cell(rownum, NameCol).value)
		ws.write(rownum, NameTypeCol, sh_OSM_links.cell(rownum, NameTypeCol).value)
		ws.write(rownum, NodesTotCol, sh_OSM_links.cell(rownum, NodesTotCol).value)
		
		# copy nodes
		nodesTot = int(sh_OSM_links.cell(rownum, NodesTotCol).value)
		nodesRead = 0
		tempNodesRead = 0
		extraRow = 0
		while (nodesRead < nodesTot):
			if (tempNodesRead == 250):
				extraRow += 1
				rownum += 1
				tempNodesRead = 0
			ws.write(rownum, NodesCol + tempNodesRead, sh_OSM_links.cell(rownum, NodesCol + tempNodesRead).value)
			nodesRead += 1
			tempNodesRead += 1
		
		# define first and last nodes in link
		OSMNodeA = sh_OSM_links.cell(rownum, NodesCol).value
		if (nodesTot < 250):
			OSMNodeB = sh_OSM_links.cell(rownum, NodesCol + nodesTot - 1).value
		else:
			extra_rows = int(nodesTot / 250)
			node = nodesTot % 250
			OSMNodeB = sh_OSM_links.cell(rownum + extra_rows, NodesCol + node - 1).value
		
		get_OSM_coords(OSMNodeA)
		OSMNodeALat = tempLat
		OSMNodeALon = tempLon
		
		get_OSM_coords(OSMNodeB)
		OSMNodeBLat = tempLat
		OSMNodeBLon = tempLon
		
		match_nodes(OSMNodeALat, OSMNodeALon)
		DynNodeA = tempNodeId
		
		match_nodes(OSMNodeBLat, OSMNodeBLon)
		DynNodeB = tempNodeId
		
		tempLanes = 0
		get_lanes(DynNodeA, DynNodeB)
		get_lanes(DynNodeB, DynNodeA)
		
		if (tempLanes == 0):
			ws.write(rownum-extraRow, LanesCol, 4)
		else:
			ws.write(rownum-extraRow, LanesCol, tempLanes)


print 'Done!'
	
w.save('OSM_links_final.xls')