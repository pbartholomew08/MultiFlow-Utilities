"""
  readGMSHMesh.py:

    read gmsh mesh and return mesh object
"""
from pyPostProc.classes.mesh import node as nodeClass
from pyPostProc.classes.mesh import face as faceClass
from pyPostProc.classes.mesh import cell as cellClass
from pyPostProc.classes.mesh import mesh as meshClass

def readNodes(meshFile, quiet = True):

  line = meshFile.readline()
  nNodes = int(line)
  if not quiet:

    print "nNodes = %i" % nNodes

  nodes = []
  quit = False
  while not quit:

    line = meshFile.readline()
    
    if line.find("$EndNodes"):

      quit = True
      continue

    else:

      nodeData = line.split()

      idx = int(nodeData[0])
      X = float(nodeData[1])
      Y = float(nodeData[2])
      Z = float(nodeData[3])

      nodes.append(nodeClass(X, Y, Z, idx))
      if not quiet:
        print "node: %i %e %e %e" % (idx, X, Y, Z)

def readMesh(filePath, quiet = True):

  # KEYWORDS in gmsh
  KEYWORDS = ["$Nodes\n"]
  funcArr = [readNodes]

  # Open and read file
  with open(filePath, "r") as meshFile:

    quit = False
    while not quit:

        line = meshFile.readline()
        if not line:

          quit = True
          continue

        if line in KEYWORDS:
          
          func = funcArr[KEYWORDS.index(line)]
          func(meshFile, quiet)

