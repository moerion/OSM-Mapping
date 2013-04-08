# This script extracts link information from the OSM .xml file and writes it in a .csv file.

print 'Importing links...'

import string
import csv

# format csv output file
f = csv.writer(open("OSM_links.csv", "wb"), delimiter=',', lineterminator='\n')

# node counter and array
nodesTot = 0
nodes = []

# boolean for link
link = False

# write column titles
f.writerow(['Link ID','Type','Name','Name Type', 'Total Nodes', 'Nodes'])

# open file to read
infile = open('map.xml', 'r')
for line in infile:
	
		
	str = '<way id="'
	strIndex = string.find(line, str)
	
	# new Link entry
	if (strIndex != -1):
				
		# reset counters and boolean
		nodesTot = 0
		nodes = []
		linkId = ''
		linkName = ''
		linkType =''
		linkNameType = ''
		link = True
		
		strLen = len(str)
		str = '" user="'
		
		# store Link ID 
		linkId = line[strIndex+strLen : string.find(line, str)]
		
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
				
					
				# add new node to list
				nodes.append(line[strIndex+strLen : string.find(line, str)])

				# increment node counters
				nodesTot += 1
				
			else:
				
				str = '<tag k="highway" v="'
				strIndex = string.find(line, str)
				
				# Type tag
				if (strIndex != -1):
					
					strLen = len(str)
					str = '"/>'
					
					# store Link Type
					linkType = line[strIndex+strLen : string.find(line, str)]

					# update boolean
					highway = True
				
				else:
					
					str = '<tag k="tiger:name_base" v="'
					strIndex = string.find(line, str)
				
					# Name tag
					if (strIndex != -1):
				
						strLen = len(str)
						str = '"/>'
					
						# store Link Name
						linkName = line[strIndex+strLen : string.find(line, str)]
						
					else:
					
						str = '<tag k="tiger:name_type" v="'
						strIndex = string.find(line, str)
				
						# Name Type tag
						if (strIndex != -1):
				
							strLen = len(str)
							str = '"/>'
					
							# store Link Name Type
							linkNameType = line[strIndex+strLen : string.find(line, str)]

						else:
							
							str = '<tag k="name" v="'
							strIndex = string.find(line, str)
							
							# Name tag
							if (strIndex != -1):
						
								strLen = len(str)
								str = '"/>'
								
								# store Link Name
								linkName = line[strIndex+strLen : string.find(line, str)]
							
							else:
								
								str = '</way>'
								strIndex = string.find(line, str)
								
								# end of Link entry
								if (strIndex != -1):
									
									# write Link Information to file
									if ((linkType != '')&(linkName != '')):
										f.writerow([linkId, linkType, linkName, linkNameType, nodesTot] + nodes)
									
									# update link boolean
									link = False
			
infile.close()
print 'Done!'
	

		