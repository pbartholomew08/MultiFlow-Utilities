"""
  writeVTUMesh:

    Takes a mesh object and writes it out in VTU format
"""
def writeNodes(mesh, meshFiles):

  nNodes = mesh.nNodes

  # Write node header
  meshFile.write('\t\t\t<Points>\n')

  # Write end of nodes
  meshFile.write('\t\t\t</Points>\n')

def writeMeshData(mesh, meshFile):

  nNodes = mesh.nNodes
  nCells = mesh.nCells
  meshFile.write('\t\t<Piece NumberOfPoints="%i" NumberOfCells="%i">\n') % (nNodes, nCells)

  # Write nodes
  # Write cells

  meshFile.write('\t\t</Piece>\n')

def writeVTUMesh(mesh, filePath):

  # Open meshFile
  with open(filePath, "w") as meshFile:

    # Write header
    meshFile.write('<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">\n')
    meshFile.write('\t<UnstructuredGrid>\n')

    # Write mesh data
    writeMeshData(mesh, meshFile)

    # Write end of file
    meshFile.write('\t</UnstructuredGrid>\n')
    meshFile.write('</VTKFile>\n')
