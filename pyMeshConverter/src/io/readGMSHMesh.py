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

      nodes.append([idx, X, Y, Z])

  # Error checking
  assert(len(nodes) == nNodes)
  print "nNodes = %i" % nNodes

  return [nodes], ["nodes"]

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
        faces.append([nFaces, nodes])
        elem.append(["face", nFaces])

        nFaces += 1

      elif (elemType > 3) and (elemType < 8):

        # Volume element: ( 4 is TET, 5 is HEX, 6 is WEDGE, 7 is 5-node pyramid)
        cells.append([nCells, nodes])
        elem.append(["cell", nCells])

        nCells += 1

  print "nCells = %i" % nCells
  print "nFaces = %i" % nFaces

  return [cells, faces], ["cells", "faces"]

def readMesh(filePath, quiet = True):

  # KEYWORDS in gmsh
  KEYWORDS = ["$Nodes\n", "$Elements\n"]
  funcArr = [readNodes, readElems]

  meshData = {}

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
          data, keys = func(meshFile, quiet)

          nFields = len(data)
          for d in range(nFields):

            meshData[keys[d]] = data[d]

  # Make node, cell, face arrays
  nNodes = len(meshData["nodes"])
  nCells = len(meshData["cells"])
  nFaces = len(meshData["faces"])

  nodes = [0] * nNodes
  cells = [0] * nCells
  faces = [0] * nFaces

  for n in range(nNodes):

    idx = meshData["nodes"][n][0]
    x = meshData["nodes"][n][1]
    y = meshData["nodes"][n][2]
    z = meshData["nodes"][n][2]

    nodes[n] = nodeClass(x, y, z, idx)

  for c in range(nCells):

    idx = meshData["cells"][c][0]
    nodeArr = meshData["cells"][c][1]

    cellNodes = []
    for n in nodeArr:

      cellNodes.append(nodes[n - 1])

    cells[c] = cellClass(cellNodes, idx)

  for f in range(nFaces):

    idx = meshData["faces"][f][0]
    nodeArr = meshData["faces"][f][1]

    faceNodes = []
    for n in nodeArr:

      faceNodes.append(nodes[n - 1])

    faces[f] = faceClass(faceNodes, idx)

  # Link cells / faces
  print "Linking cells-faces"
  complete = 0
  completeOld = 0
  nFacesInv = 1.0 / nFaces
  for f in range(nFaces):

    faceNodeArr = faces[f].node

    for c in range(nCells):

      cellNodeArr = cells[c].node

      if set(faceNodeArr).issubset(cellNodeArr):

        faces[f].linkCell(c)
        cells[c].linkFace(f)

      if faces[f].nCells == 2:

        break

    assert(faces[f].nCells > 0)
    assert(faces[f].nCells < 3)

    if faces[f].nCells == 2:

      # Not boundary face
      faces[f].bndFlg = 0

      # Cells must be neighbours 
      c1 = faces[f].cell[0]
      c2 = faces[f].cell[1]

      cells[c1].linkNeighbour(c2)
      cells[c2].linkNeighbour(c1)

    elif faces[f].nCells == 1:

      # Boundary face
      faces[f].bndFlg = 1

    complete = 100 * (f * nFacesInv)
    """
    if complete > completeOld + 1:

      completeOld += 1
      print completeOld
    """

  print "Creating mesh"
  mesh = meshClass(nodes, cells, faces)

  return mesh
