# This script extracts OSM link and node information from .xls files and creates a graphical representation of the map in Blender.
# Alternate Algorithm: using angle bisectors
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
laneWidth_v_old = .01

nodeC_old = -1

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
		tmpNodesRead = 0
		
		if (nodesTot > 1):
			
			
			# create a new Street named Street-xxx
 			street = B.Object.New('Mesh', 'Street-' + name + '-' + str(newLinkId))
			mesh = B.Mesh.New('Plane')
		
			# get node information for link and draw
			while (nodesRead < nodesTot):
				if (tmpNodesRead == 250):
					tmpNodesRead = 0
					rownum += 1
					
				if (nodesRead == 0):
					nodeA = sh_links.cell(rownum, NodesCol + tmpNodesRead).value
					nodeB = sh_links.cell(rownum, NodesCol + tmpNodesRead + 1).value
					nodeC = -1
				elif (nodesRead > 0):
					nodeA = sh_links.cell(rownum, NodesCol + tmpNodesRead - 1).value
					nodeB = sh_links.cell(rownum, NodesCol + tmpNodesRead).value
					nodeC = -1
					if (nodesRead < nodesTot - 1):
						nodeC = sh_links.cell(rownum, NodesCol + tmpNodesRead + 1).value
					
				
				# get node coordinates
				for rownum1 in range(sh_nodes.nrows):
					# search for nodes in file
					if (rownum1 > 0):
						if ((nodesRead == 0)&(nodeA == sh_nodes.cell(rownum1, NodeIdCol).value)):
							
							y1 = float(sh_nodes.cell(rownum1, LatCol).value)
							x1 = float(sh_nodes.cell(rownum1, LonCol).value)
							
							x1 = (x1 + 115)* 1000+200
							y1 = (y1 - 36) * 1000-200

							street.loc = x1, y1, 0	# define object location
							
							Dx = 0
							Dy = 0
							Dx_old = 0
							Dy_old = 0
	
						elif ((nodesRead == 0)&(nodeB == sh_nodes.cell(rownum1, NodeIdCol).value)):
							
							y2 = float(sh_nodes.cell(rownum1, LatCol).value)
							x2 = float(sh_nodes.cell(rownum1, LonCol).value)
						
							x2 = (x2 + 115)* 1000+200
							y2 = (y2 - 36) * 1000-200
							
						elif ((nodeC != -1)&(nodeC == sh_nodes.cell(rownum1, NodeIdCol).value)):
							
							y3 = float(sh_nodes.cell(rownum1, LatCol).value)
							x3 = float(sh_nodes.cell(rownum1, LonCol).value)
							
							x3 = (x3 + 115)* 1000+200
							y3 = (y3 - 36) * 1000-200
				
		
				
				
				# calculations for new vertices
				if (nodeC == -1): # first or last nodes
					
					tmpDx = x2 - x1		# new Delta x
					tmpDy = y2 - y1		# new Delta y
					
					if (tmpDy == 0):
						if (tmpDx > 0):
							a1 = -1 * M.pi / 2
						else:
							a1 = M.pi / 2
								
					else:
						a1 = -1*M.atan(tmpDx/tmpDy)	# angle1 in radians
				
					offsetY = M.sin(a1) * laneWidth_v_old		# offsets for new vertices
					offsetX = M.cos(a1) * laneWidth_v_old
					
					if (nodesRead > 0):
						if (offsetY_old < 0):
							offsetY = -1*abs(offsetY)
						else:
							offsetY = abs(offsetY)
							
					
					
				else:			# intermediate nodes
					
					tmpDx = x3 - x2		# new Delta x
					tmpDy = y3 - y2		# new Delta y
					tmpDx1 = x2 - x1
					tmpDy1 = y2 - y1
					
					if (tmpDx == 0):
						if (tmpDy > 0):
							 t2 = M.pi / 2
						else:
							t2 = -1 * M.pi / 2
					else:
						r2 = (tmpDy)/(tmpDx)
						t2 = M.atan(r2)
					
					if (tmpDx1 == 0):
						if (tmpDy1 > 0):
							 t1 = M.pi / 2
						else:
							t1 = -1 * M.pi / 2
					else:
						r1 = (tmpDy1)/(tmpDx1)
						t1 = M.atan(r1)
				
					if (tmpDy1 == 0):
						if (tmpDx1 > 0):
							a1 = -1 * M.pi / 2
						else:
							a1 = M.pi / 2
					else:
						a1 = M.atan(-1*((tmpDx1)/(tmpDy1)))	# angle1 in radians
					
					#print name, nodesRead,  'y2=', y2, 'x2=', x2, 'y3=',y3, 'x3=',x3
					
					a2 = .5 * (M.pi - abs(t1 + t2))
					
					if ((t1 > 0) & (t2 < 0)):
						a2 = .5 * ((t1 + t2))

					elif((t1 < 0) & (t2 > 0)):
						a2 = .5 * (M.pi-abs(M.atan2((y2-y1),(x2-x1)) + M.atan2((tmpDy),(tmpDx))))

					elif ((t1 > 0) & (t2 > 0)):
						a2 = .5 * (M.pi + abs(t1 + t2))

					
					laneWidth_v = laneWidth_v_old * 1/(M.cos(abs(a2-a1)))
					
					offsetX = laneWidth_v * M.cos(a2)
					offsetY = laneWidth_v * M.sin(a2)
					
									
				Dx = Dx + tmpDx		# overall Delta x
				Dy = Dy + tmpDy		# overall Delta y
				
				
						
				
				# create object vertices
				lane = 0
				while (lane <= lanesTot):	
	
					v = [Dx_old+lane*offsetX, Dy_old+lane*offsetY, 0]
					
					lane += 1
					
					coords = [v]
					#faces = [ [i,i+1,i+3,i+2] ]
				
				
					mesh.verts.extend(coords)          # add vertices to mesh
					#mesh.faces.extend(faces)           # add faces to the mesh (also adds edges)
					
				
				lane = 0		
					
				if (nodesRead > 0):
					while (lane < lanesTot):
						
						faces = [[i, i+1, i+int(lanesTot+2), i+int(lanesTot+1)]]
							
						mesh.faces.extend(faces)           # add faces to the mesh (also adds edges)
						i += 1
						lane +=1
						if (lane == lanesTot):
							i +=1
				
				
				
				if (nodeC != -1):
					y1 = y2
					x1 = x2
					y2 = y3
					x2 = x3
					
				nodeC_old = nodeC
			
				Dx_old = Dx
				Dy_old = Dy
				
				offsetY_old = offsetY
				
				nodesRead += 1
				tmpNodesRead += 1
		
		
			
		if (nodesTot > 1):
			street.link(mesh)		# link mesh to object
			#mesh.remDoubles(LaneWidth/10)	# remove duplicate vertices from mesh object
			scene.link(street)   	# link our new object into scene	
			B.Redraw(-1)
B.Redraw(-1)
print 'Done!'