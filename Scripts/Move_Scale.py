import Blender

ob = Blender.Object.Get("Cube.001")
ob.LocX = 10
ob.LocY = 15
ob.SizeX = .5
ob.SizeY = .5
ob.SizeZ = .5

print 'Done!'