# This script extracts link information from the OSM .xml file and writes it in a .xls file.

print 'Running...'

# xlwt library found at (http://pypi.python.org/pypi/xlwt)
import xlwt
import string

# format xls output file
w = xlwt.Workbook()
ws = w.add_sheet('Links')

# store used column numbers
LinkIdCol = 0
LanesCol = 1
TypeCol = 2
NameCol = 3
NameTypeCol = 4
NodesTotCol = 5
NodesCol = 6

# row counters
row = 0
extraRow = 0

# node counters
nodesTot = 0
tmpNodesTot = 0

# boolean for link
link = False

# write column titles
ws.write(row, LinkIdCol, 'Link ID')
ws.write(row, LanesCol, 'Lanes')
ws.write(row, TypeCol, 'Type')
ws.write(row, NameCol, 'Name')
ws.write(row, NameTypeCol, 'Name Type')
ws.write(row, NodesTotCol, 'Total Nodes')
ws.write(row, NodesCol, 'Nodes')

# skip a row
row += 1

# open file to read
#try:
infile = open('map.xml', 'r')
for line in infile:
	
		
	str = '<way id="'
	strIndex = string.find(line, str)
	
	# new Link entry
	if (strIndex != -1):
				
		# update counters and boolean
		nodesTot = 0
		tmpNodesTot = 0
		row += 1
		extraRow = 0
		link = True
		
		strLen = len(str)
		str = '" user="'
		
		# write Link IDs to file
		ws.write(row, LinkIdCol, line[strIndex+strLen : string.find(line, str)])
		
	else:
		
		if (link == True):
			str = '<nd ref="'
			strIndex = string.find(line, str)
			
			# new Node entry
			if (strIndex != -1):
				
				strLen = len(str)
				str = '"/>'
				
				#print nodesTot
				#print line
				
				if (tmpNodesTot == 250):
					row += 1
					extraRow += 1
					tmpNodesTot = 0
					
				# add new node to list
				ws.write(row, NodesCol+ tmpNodesTot, line[strIndex+strLen : string.find(line, str)])
				
				# increment node counters
				nodesTot += 1
				tmpNodesTot += 1
				
			else:
				
				str = '<tag k="highway" v="'
				strIndex = string.find(line, str)
				
				# Type tag
				if (strIndex != -1):
					
					strLen = len(str)
					str = '"/>'
					
					# write Link Type to file
					ws.write(row-extraRow, TypeCol, line[strIndex+strLen : string.find(line, str)])
					
					# update boolean
					highway = True
				
				else:
					
					str = '<tag k="tiger:name_base" v="'
					strIndex = string.find(line, str)
				
					# Name tag
					if (strIndex != -1):
				
						strLen = len(str)
						str = '"/>'
					
						# write Link Name to file
						ws.write(row-extraRow, NameCol, line[strIndex+strLen : string.find(line, str)])
						
					else:
					
						str = '<tag k="tiger:name_type" v="'
						strIndex = string.find(line, str)
				
						# Name Type tag
						if (strIndex != -1):
				
							strLen = len(str)
							str = '"/>'
					
							# write Link Name Type to file
							ws.write(row-extraRow, NameTypeCol, line[strIndex+strLen : string.find(line, str)])
							
						else:
							
							str = '</way>'
							strIndex = string.find(line, str)
							
							# end of Link entry
							if (strIndex != -1):
								
								# write Total Nodes to file
								ws.write(row-extraRow, NodesTotCol, nodesTot)
								
								# update link boolean
								link = False
			
#except:
	#print line
	#print 'Error reading file'
#else:
infile.close()
print 'Done!'
	
w.save('OSM_links.xls')
		