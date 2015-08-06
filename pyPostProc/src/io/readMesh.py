import h5py
from pyPostProc.classes import mesh as meshClasses

def readHDF5Mesh(meshFile, quiet = False):
  """
    Reads MultiFlow Unstructured mesh file
  """

  # Open mesh
  mesh = h5py.File(meshFile, "r")

  # Mesh info =================================  #
  meshData = mesh["/meshData"]

  if not quiet:
    print "Successfully opened mesh: %s" % meshFile

  nNodes = int(meshData[0][0])
  nCells = int(meshData[1][0])
  nFaces = int(meshData[2][0])
  cellType = meshData[3][0]  # 4 = tet, 5 = hex, 8 = poly - maybe? Seems to be 8 for a hex mesh...
  del(meshData)

  if not quiet:
    print "Mesh Data:"
    print "\tnNodes: %i" % nNodes
    print "\tnCells: %i" % nCells
    print "\tnFaces: %i" % nFaces

  # Read nodes ================================= #
  if not quiet:
    print "Reading nodes"
  nodes_XYZ = mesh["/nodes"]
  assert(len(nodes_XYZ) / 3 == nNodes)
  nodes = [0] * nNodes
  nodeCtr = 0
  for n in range(nNodes):

    X = float(nodes_XYZ[nodeCtr + 0][0])
    Y = float(nodes_XYZ[nodeCtr + 1][0])
    Z = float(nodes_XYZ[nodeCtr + 2][0])

    nodeCtr += 3

    nodes[n] = meshClasses.node(X, Y, Z, n)

  del(nodes_XYZ)

  # Read cells ================================= #
  if not quiet:
    print "Reading cells"
  cellDataArr = mesh["/cells"]
  cellNodePtr = mesh["/cellNodePtr"]
  assert(len(cellNodePtr) == nCells + 1)
  cells = [0] * nCells
  cellCtr = 0
  for c in range(nCells):

    cell_nNodes = int(cellNodePtr[c + 1][0] - cellNodePtr[c][0])
    
    # First value in cellDataArr is the cell type - not of interest
    cellCtr += 1

    # This is followed by the node indices
    cell_nodes = [0] * cell_nNodes
    for n in range(cell_nNodes):

      idx = int(cellDataArr[cellCtr][0])
      cell_nodes[n] = nodes[idx]
      cellCtr += 1

    cells[c] = meshClasses.cell(cell_nodes, c)

  del(cellDataArr)
  del(cellNodePtr)

  # Read faces ================================= #
  if not quiet:
    print "Reading faces"
  faceDataArr = mesh["/faces"]
  faceNodePtr = mesh["/faceNodePtr"]
  assert(len(faceNodePtr) == nFaces + 1)
  faces = [0] * nFaces
  faceCtr = 0
  for f in range(nFaces):

    face_nNodes = int(faceNodePtr[f + 1][0] - faceNodePtr[f][0])

    face_nodes = [0] * face_nNodes
    for n in range(face_nNodes):

      idx = int(faceDataArr[faceCtr])
      face_nodes[n] = nodes[idx]
      faceCtr += 1

    faces[f] = meshClasses.face(face_nodes, f)

  # Close mesh ================================= #
  mesh.close()
  if not quiet:
    print "Closed mesh file"

  # Construct mesh ============================= #
  if not quiet:
    print "Constructing mesh"
  mesh = meshClasses.mesh(nodes, faces, cells)

  return mesh
