# This script extracts OSM link information from a .xls file and writes only the links that are roads into a new .xls file.

print 'Cleaning links...'

# xlrd library found at (http://pypi.python.org/pypi/xlrd)
import xlrd

# xlwt library found at (http://pypi.python.org/pypi/xlwt)
import xlwt

# open workbook
wb = xlrd.open_workbook('OSM_links.xls')

# load sheet
sh = wb.sheet_by_index(0)

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

# row counter
row = 0

# node counters
nodesTot = 0
nodes = 0
tmpNodes = 0

# write column titles
ws.write(row, LinkIdCol, 'Link ID')
ws.write(row, LanesCol, 'Lanes')
ws.write(row, TypeCol, 'Type')
ws.write(row, NameCol, 'Name')
ws.write(row, NameTypeCol, 'Name Type')
ws.write(row, NodesTotCol, 'Total Nodes')
ws.write(row, NodesCol, 'Nodes')

# skip a row
row += 2

for rownum in range(sh.nrows):
    	
	if (rownum > 1):
		
		# if Link is a road
		if (sh.cell(rownum, NameCol).value != ''):
			# copy cells
			ws.write(row, LinkIdCol, sh.cell(rownum, LinkIdCol).value)
			ws.write(row, LanesCol, sh.cell(rownum, LanesCol).value)
			ws.write(row, TypeCol, sh.cell(rownum, TypeCol).value)
			ws.write(row, NameCol, sh.cell(rownum, NameCol).value)
			ws.write(row, NameTypeCol, sh.cell(rownum, NameTypeCol).value)
			
			# copy Nodes
			nodesTot = sh.cell(rownum, NodesTotCol).value
			ws.write(row, NodesTotCol, nodesTot)
			nodes = 0
			tmpNodes = 0
			while (nodes <= nodesTot):
				if (tmpNodes == 250):
					row += 1
					rownum += 1
					tmpNodes = 0
				ws.write(row, NodesCol+tmpNodes, sh.cell(rownum, NodesCol+tmpNodes).value)
				nodes += 1
				tmpNodes +=1
			
			# increment row	
			row +=1

print 'Done!'
	
w.save('OSM_links_clean.xls')