# This script extracts OSM link and node information from .csv files and creates a graphical representation of the map in Blender.
# Alternate Algorithm: using angle bisectors

# CSV library
import csv

# Blender library
import Blender as B

# math library
import math as M

# format csv link file reader
linkReader = csv.reader(open('OSM_links_final.csv', 'rb'))

# format csv node file reader
nodeReader = csv.reader(open('OSM_nodes.csv', 'rb'))

# store used column numbers for links file
NewLinkIdCol = 0
OSMLinkIdCol = 1
TypeCol = 2
NameCol = 3
NameTypeCol = 4
LanesCol = 5
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

linkRowNum = 0
# get link information from file
for linkRow in linkReader:
    
	# skip header
	if (linkRowNum > 0):
		# get information for new link
		newLinkId = linkRow[0]
		osmLinkId = linkRow[1]
		type = linkRow[2]
		name = linkRow[3]
		nameType = linkRow[4]
		lanesTot = int(linkRow[5])
		nodesTot = int(linkRow[6])
		nodes = linkRow[7:(7+nodesTot)]
		#print nodes
		#print nodesTot
		
		scene = B.Scene.getCurrent()
		
		# node count
		nodesRead = 0
		# node index in array
		i = 0
		# node index for faces
		n = 0
		
		if (nodesTot > 1):
			
			
			# create a new Street named Street-xxx
 			street = B.Object.New('Mesh', 'St-' + name + '-' + str(newLinkId))
			mesh = B.Mesh.New('Plane')
		
			# get node information for link and draw
			while (i < nodesTot):
				if (i == 0):
					nodeA = nodes[i]
					nodeB = nodes[i+1]
					nodeC = -1
				elif (i > 0):
					nodeA = nodes[i-1]
					nodeB = nodes[i]
					nodeC = -1
					if (i < (nodesTot - 1)):
						nodeC = nodes[i+1]
					
				nodeRowNum = 0
				
				
				# format csv node file reader
				nodeReader = csv.reader(open('OSM_nodes.csv', 'rb'))
				
				# get node coordinates
				for nodeRow in nodeReader:
					# search for nodes in file
					if (nodeRowNum > 0):
						if ((i == 0)&(nodeA == nodeRow[0])):
							
							y1 = float(nodeRow[1])
							x1 = float(nodeRow[2])
							
							x1 = (x1 + 115)* 1000+200
							y1 = (y1 - 36) * 1000-200

							street.loc = x1, y1, 0	# define object location
							
							Dx = 0
							Dy = 0
							Dx_old = 0
							Dy_old = 0
	
						elif ((i == 0)&(nodeB == nodeRow[0])):
							
							y2 = float(nodeRow[1])
							x2 = float(nodeRow[2])
						
							x2 = (x2 + 115)* 1000+200
							y2 = (y2 - 36) * 1000-200
							
						elif ((nodeC != -1)&(nodeC == nodeRow[0])):
							
							y3 = float(nodeRow[1])
							x3 = float(nodeRow[2])
							
							x3 = (x3 + 115)* 1000+200
							y3 = (y3 - 36) * 1000-200
							
					nodeRowNum += 1
				
				# calculations for new vertices
				if (nodeC == -1): # first or last nodes
					#print 'here', i, nodeC
					tmpDx = x2 - x1		# new Delta x
					tmpDy = y2 - y1		# new Delta y
					
					if (tmpDy == 0):
						if (tmpDx > 0):
							a1 = -1 * M.pi / 2
						else:
							a1 = M.pi / 2
								
					else:
						a1 = -1*M.atan2(tmpDx,tmpDy)	# angle1 in radians
				
					offsetY = M.sin(a1) * laneWidth_v_old		# offsets for new vertices
					offsetX = M.cos(a1) * laneWidth_v_old
					
				#	if (nodesRead > 0):
				#		if (offsetY_old < 0):
				#			offsetY = -1*abs(offsetY)
				#		else:
				#			offsetY = abs(offsetY)
							
					
					
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
						t2 = M.atan2((tmpDy),(tmpDx))
					
					if (tmpDx1 == 0):
						if (tmpDy1 > 0):
							 t1 = M.pi / 2
						else:
							t1 = -1 * M.pi / 2
					else:
						t1 = M.atan2((tmpDy1),(tmpDx1))
				
					if (tmpDy1 == 0):
						if (tmpDx1 > 0):
							a1 = -1 * M.pi / 2
						else:
							a1 = M.pi / 2
					else:
						a1 = -1 * M.atan2((tmpDx1),(tmpDy1))	# angle1 in radians
					
					#print name, nodesRead,  'y2=', y2, 'x2=', x2, 'y3=',y3, 'x3=',x3
					
					a2 = .5 * (M.pi + (t1 + t2))
					
					#if ((t1 > 0) & (t2 < 0)):
					#	a2 = M.pi/2 - .5 * ((t1 - t2))

					#elif((t1 < 0) & (t2 > 0)):
					#	a2 = .5 * (M.pi-abs(M.atan2((y2-y1),(x2-x1)) + M.atan2((tmpDy),(tmpDx))))

					#elif ((t1 > 0) & (t2 > 0)):
					#	a2 = .5 * (M.pi + abs(t1 + t2))

					
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
						print lanesTot, lane, nodesRead, i
						faces = [[n, n+1, n+int(lanesTot+2), n+int(lanesTot+1)]]
							
						mesh.faces.extend(faces)           # add faces to the mesh (also adds edges)
						n += 1
						lane +=1
						if (lane == lanesTot):
							n +=1
				
				
				
				if (nodeC != -1):
					y1 = y2
					x1 = x2
					y2 = y3
					x2 = x3
					
				nodeC_old = nodeC
			
				Dx_old = Dx
				Dy_old = Dy
				
				offsetY_old = offsetY
				
			
				# update node index
				i +=1
					
				# update node count
				nodesRead += 1
				
		if (nodesTot > 1):
			street.link(mesh)		# link mesh to object
			#mesh.remDoubles(LaneWidth/10)	# remove duplicate vertices from mesh object
			scene.link(street)   	# link our new object into scene	
			B.Redraw(-1)
			
	# update link file row counter
	linkRowNum += 1
		
B.Redraw(-1)
print 'Done!'