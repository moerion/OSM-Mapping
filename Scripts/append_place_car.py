# This script will append a scaled car object to the map and move it to a specified location

import Blender
from Blender import Library, Window, Draw, BGL, Camera, Object



#2 import selected _OBJECT_ data.
def open_library(name):
 global object_list, already_imported
 object_list=[]
 already_imported = 1

 Library.Open(name) # opens the library file
 groups = Library.LinkableGroups()

 data_Type = 'Object'

#3 _append_ OBJECTS to new file.
 # if the objects are 'Object' (can change to Mesh, Arm, light etc...)
 if data_Type in groups:
   for obname in Library.Datablocks(data_Type):
     Library.Load(obname, data_Type, 0) # note the 0...
     # add the objec to a list so imported objects
     # _only_ are renamed.........
     object_list.append(obname)
   Library.Update()

 Library.Close()
 Window.RedrawAll()

#
# Main:
#

print 'Importing...'

object_list=[]
already_imported = 0

name = "C:\Users\Morris\Dropbox\TRC\OSM Mapping\ScaledScene_car.blend"

#1 SELECT file to append from.
open_library(name)


# Move object to specified coordinates

ob = Blender.Object.Get("Cube.001")
ob.LocX = 49.34
ob.LocY = -84

# Set object rotation

ob.RotZ = -.05



print 'Done!'