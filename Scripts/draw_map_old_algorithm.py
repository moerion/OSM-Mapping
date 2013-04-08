# This script extracts OSM link and node information from .xls files and creates a graphical representation of the map in Blender.

# xlrd library found at (http://pypi.python.org/pypi/xlrd)
import xlrd

# Blender library
import Blender as B

# math library
import math as M

# open workbooks
wb_links = xlrd.open_workbook('OSM_links_final.xls')
wb_nodes = xlrd.open_workbook('OSM_nodes.xls')

# load sheets
sh_links = wb_links.sheet_by_index(0)
sh_nodes = wb_nodes.sheet_by_index(0)

# store used column numbers for links file
NewLinkIdCol = 0
OSMLinkIdCol = 1
LanesCol = 2
TypeCol = 3
NameCol = 4
NameTypeCol = 5
NodesTotCol = 6
NodesCol = 7

# store used column numbers for nodes file
NodeIdCol = 0
LatCol = 1
LonCol = 2
PropCol = 3

# node counters
nodesTot = 0			# total nodes per current link
nodesRead = 0			# number of nodes read from current link

# constants
LaneWidth = .01

#boolean
flipped = False

#
# main
#

print 'Running...'
	# clear scene
scns = B.Scene.Get()	# get a list of all scenes in Blender
for i in scns:			# get each scene in the list
	scn = i
	obs = list(scn.objects)		# get a list of all objects in scene
	for j in obs:				# get each object in the scene
		scn.unlink(j)			# unlink the object from the scene

B.Redraw(-1) 		# update all of the views in the user inteface

	# get link information from file
for rownum in range(sh_links.nrows):
    	
	if (rownum > 1):
		# get information for new link
		newLinkId = sh_links.cell(rownum, NewLinkIdCol).value
		osmLinkId = sh_links.cell(rownum, OSMLinkIdCol).value
		lanesTot = sh_links.cell(rownum, LanesCol).value
		type = sh_links.cell(rownum, TypeCol).value
		name = sh_links.cell(rownum, NameCol).value
		nameType = sh_links.cell(rownum, NameTypeCol).value
		nodesTot = sh_links.cell(rownum, NodesTotCol).value
		
		scene = B.Scene.getCurrent()
	
		
		i = 0
		nodesRead = 0
		
		if (nodesTot > 1):
			
			
			# create a new Street named Street-xxx
 			street = B.Object.New('Mesh', 'Street-' + name + '-' + str(newLinkId))
			mesh = B.Mesh.New('Plane')
		
			# get node information for link and draw
			while (nodesRead < nodesTot):
				nodeA = sh_links.cell(rownum, NodesCol + nodesRead).value		
				if (nodesRead < nodesTot - 1):
					nodeB = sh_links.cell(rownum, NodesCol + nodesRead + 1).value
				
				# get node coordinates
				for rownum1 in range(sh_nodes.nrows):
					# search for nodes in file
					if (rownum1 > 0):
						if (nodeA == sh_nodes.cell(rownum1, NodeIdCol).value):
							if (nodesRead == 0):
								y1 = float(sh_nodes.cell(rownum1, LatCol).value)
								x1 = float(sh_nodes.cell(rownum1, LonCol).value)
								
								
								
								x1 = (x1 + 115)* 1000+200
								y1 = (y1 - 36) * 1000-200
	
								street.loc = x1, y1, 0	# define object location
								
								Dx = 0
								Dy = 0
	
						elif (nodeB == sh_nodes.cell(rownum1, NodeIdCol).value):
							y2 = float(sh_nodes.cell(rownum1, LatCol).value)
							x2 = float(sh_nodes.cell(rownum1, LonCol).value)
							
							x2 = (x2 + 115)* 1000+200
							y2 = (y2 - 36) * 1000-200
				
			
				
				
				# calculations for new vertices
				if (nodesRead < nodesTot -1):
					tmpDx = x2 - x1		# new Delta x
					tmpDy = y2 - y1		# new Delta y
				
					Dx = Dx + tmpDx		# overall Delta x
					Dy = Dy + tmpDy		# overall Delta y
				
				
					if (tmpDy == 0):
						if (tmpDx > 0):
							a1 = M.pi/2
						elif (tmpDx < 0):
							a1 = -1 * M.pi/2
						else:
							a1 = 0
					else:
						a1 = M.atan(tmpDx/tmpDy)	# angle1 in radians
				
					
					offsetY = abs(M.sin(a1) * LaneWidth)		# offsets for new vertices
					#if (tmpDy < 0):
					#	offsetY = -(offsetY)
					offsetX = abs(M.cos(a1) * LaneWidth)
					if (((tmpDx < 0)&(tmpDy < 0))|((tmpDx > 0)&(tmpDy > 0))):
						offsetX = -(offsetX)
						offsetY = -(offsetY)
						flipped = True
					else:
						flipped = False
				
						
				
				# create object vertices
				lane = 0
				while (lane <= lanesTot):	
					if (nodesRead == 0):
						v = [lane*offsetX, lane*offsetY, 0]
					else:
						v = [old_Dx + lane*old_offsetX, old_Dy + lane*old_offsetY, 0]
					
					lane += 1
					
					coords = [v]
					#faces = [ [i,i+1,i+3,i+2] ]
				
				
					mesh.verts.extend(coords)          # add vertices to mesh
					#mesh.faces.extend(faces)           # add faces to the mesh (also adds edges)
					
				
				lane = 0		
					
			
				
				if (nodesRead > 0):
					while (lane < lanesTot):
						if (old_flipped == True):
							if (old_old_flipped == False):
								faces = [[int(i%(2*(lanesTot+1)) + (lanesTot+1)*(nodesRead-1)), int(i%(2*(lanesTot+1)) + (lanesTot+1)*(nodesRead-1) +1), int(2*(lanesTot+1) - i%(2*(lanesTot+1)) -2 +(nodesRead-1)*(lanesTot+1)), int(2*(lanesTot+1) - i%(2*(lanesTot+1)) -1 +(nodesRead-1)*(lanesTot+1))]]
								
							else:
								faces = [[i, i+1, i+int(lanesTot+2), i+int(lanesTot+1)]]
						else:
							if (old_old_flipped == True):
								faces = [[i, i+1, int(i+(2*(lanesTot)-2*(i%(lanesTot+1)))),  int(i+(2*(lanesTot)-2*(i%(lanesTot+1)) +1))]]
								
							else:
								faces = [[i, i+1, i+int(lanesTot+2), i+int(lanesTot+1)]]
							
						mesh.faces.extend(faces)           # add faces to the mesh (also adds edges)
						i += 1
						lane +=1
						if (lane == lanesTot):
							i +=1
				
				y1 = y2
				x1 = x2
			
				old_offsetY = offsetY			# save calculated offsets for new road segment
				old_offsetX = offsetX
				
				old_Dx = Dx
				old_Dy = Dy
				
				#print name, flipped
				
				if (nodesRead > 0):
					old_old_flipped = old_flipped
				else:
					old_old_flipped = flipped
					
				old_flipped = flipped
				
				
				
				
				nodesRead += 1
		
		
			
		if (nodesTot > 1):
			street.link(mesh)		# link mesh to object
			#mesh.remDoubles(LaneWidth/10)	# remove duplicate vertices from mesh object
			scene.link(street)   	# link our new object into scene	
			B.Redraw(-1)
B.Redraw(-1)
print 'Done!'