# This script extracts node information from the OSM .xml file and writes it in a .xls file.

# xlwt library found at (http://pypi.python.org/pypi/xlwt)
import xlwt
import string

# format xls output file
w = xlwt.Workbook()
ws = w.add_sheet('Nodes')

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
ws.write(row, NodeIdCol, 'Node ID')
ws.write(row, LatCol, 'Latitude')
ws.write(row, LonCol, 'Longitude')
ws.write(row, PropCol, 'Properties')

# open file to read
try:
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
				ws.write(row, PropCol, line[strIndex+strLen : string.find(line, str)])
			
		node = False
		
		str = '<node id="'
		strIndex = string.find(line, str)
		
		# new Node entry
		if (strIndex != -1):
			node = True
			row += 1
			strLen = len(str)
			str = '" lat="'
			# write Node IDs to file
			ws.write(row, NodeIdCol, line[strIndex+strLen : string.find(line, str)])
			
			strIndex = string.find(line, str)
			if (strIndex != -1):
				strLen = len(str)
				str = '" lon="'
				ws.write(row, LatCol, line[strIndex+strLen : string.find(line, str)])
				
				strIndex = string.find(line, str)
				if (strIndex != -1):
					strLen = len(str)
					str = '" user="'
					ws.write(row, LonCol, line[strIndex+strLen : string.find(line, str)])
				
except:
	print 'Error reading file'
else:
	infile.close()
	print 'Done!'
	
w.save('OSM_nodes.xls')
		