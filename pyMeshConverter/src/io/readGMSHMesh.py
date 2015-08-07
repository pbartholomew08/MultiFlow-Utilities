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
    
    if line.find("$EndNodes") != -1:

      quit = True
      continue

    else:

      nodeData = line.split()

      idx = int(nodeData[0])
      X = float(nodeData[1])
      Y = float(nodeData[2])
      Z = float(nodeData[3])

      nodes.append(nodeClass(X, Y, Z, idx))

  # Error checking
  assert(len(nodes) == nNodes)
  print "nNodes = %i" % nNodes

def readElems(meshFile, quiet = True):

  line = meshFile.readline()
  nElem = int(line)
  if not quiet:

    print "nElem = %i" %nCells

  elem = []
  cells = []
  faces = []
  nCells = 0
  nFaces = 0
  quit = False
  while not quit:

    line = meshFile.readline()

    if line.find("$EndElements") != -1:

      quit = True
      continue

    else:

      elemData = line.split()

      idx = int(elemData[0])
      elemType = int(elemData[1])
      nTags = int(elemData[2])
      entry = 3
      for tag in range(nTags):
        entry += 1
      nodes = []
      for n in range(entry, len(elemData)):
        nodes.append(int(elemData[n]))
      nNodes = len(nodes)

      if (elemType == 2) or (elemType == 3):

        # Face ( 2 is triangle, 3 is quadrangle )
        faces.append(faceClass(nodes, nFaces))
        elem.append(["face", nFaces])

        nFaces += 1

      elif (elemType > 3) and (elemType < 8):

        # Volume element: ( 4 is TET, 5 is HEX, 6 is WEDGE, 7 is 5-node pyramid)
        cells.append(cellClass(nodes, nCells))
        elem.append(["cell", nCells])

        nCells += 1

  print "nCells = %i" % nCells
  print "nFaces = %i" % nFaces

def readMesh(filePath, quiet = True):

  # KEYWORDS in gmsh
  KEYWORDS = ["$Nodes\n", "$Elements\n"]
  funcArr = [readNodes, readElems]

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

