# This script extracts link information from a .xls file and writes only the links that are roads into a new .xls file.

# xlrd library found at (http://pypi.python.org/pypi/xlrd)
import xlrd

# xlwt library found at (http://pypi.python.org/pypi/xlwt)
import xlwt

# open workbook
wb = xlrd.open_workbook('Node and Link Properties.xls')

# load sheet
sh = wb.sheet_by_index(0)

# format xls output file
w = xlwt.Workbook()
ws = w.add_sheet('Node Coordinates')

# store used column numbers
NodeIdCol = 0
TDMLonCol = 1
TDMLatCol = 2
DynLonCol = 4
DynLatCol = 5

# store constants
factor = 3.04220796
offsetLon = -115647758
offsetLat = 35583501

# write column titles
ws.write(0, 1, 'TDM')
ws.write(0, 4, 'DynusT')
ws.write(1, NodeIdCol, 'Node ID')
ws.write(1, TDMLonCol, 'Longitude')
ws.write(1, TDMLatCol, 'Latitude')
ws.write(1, DynLonCol, 'Longitude')
ws.write(1, DynLatCol, 'Latitude')

for rownum in range(sh.nrows):
    	
	if (rownum > 1):
		
		# write Node ID
		ws.write(rownum, NodeIdCol, sh.cell(rownum, 5).value)
		
		# copy DynusT coordinates
		ws.write(rownum, DynLonCol, sh.cell(rownum, 6).value)
		ws.write(rownum, DynLatCol, sh.cell(rownum, 7).value)
		
		# calculate and write TDM coordinates
		ws.write(rownum, TDMLonCol, ((sh.cell(rownum, 6).value) * factor + offsetLon)/ 1000000)
		ws.write(rownum, TDMLatCol, ((sh.cell(rownum, 7).value) * factor + offsetLat)/ 1000000)

print 'Done!'
	
w.save('DynusT_nodes.xls')