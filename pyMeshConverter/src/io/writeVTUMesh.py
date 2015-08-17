"""
  writeVTUMesh:

    Takes a mesh object and writes it out in VTU format
"""
def writeNodes(mesh, meshFile):

  nNodes = mesh.nNodes

  # Write node header
  meshFile.write('\t\t\t<Points>\n')
  meshFile.write('\t\t\t\t<DataArray NumberOfComponents="3" type="Float32 format="ascii">\n')

  # Write node data
  for i in range(nNodes):
    
    meshFile.write('\t\t\t\t\t')
    for j in range(3):

      meshFile.write('%e ' % mesh.nodes[i].X[j])

    meshFile.write('\n')

  # Write end of nodes
  meshFile.write('\t\t\t\t</DataArray>\n')
  meshFile.write('\t\t\t</Points>\n')

def writeCells(mesh, meshFile):

  nCells = mesh.nCells

  # Write cell header
  meshFile.write('\t\t\t<Cells>\n')

  # Write connectivity
  meshFile.write('\t\t\t\t<DataArray type="Int32" Name="connectivity">\n')

  for i in range(nCells):

    meshFile.write('\t\t\t\t\t')
    
    nodes = mesh.cells[i].nodes
    nNodes = len(nodes)
    for j in range(nNodes):

      meshFile.write('%i ' % nodes[j])

    meshFile.write('\n')

  meshFile.write('\t\t\t\t</DataArray>\n')

  # Write offsets
  meshFile.write('\t\t\t\t<DataArray type="Int32" Name="offsets">\n')

  for i in range(nCells):

    meshFile.write('\t\t\t\t\t')

    nNodes = len(mesh.cells[i].nodes)
    meshFile.write('%i\n' % nNodes)

  meshFile.write('\t\t\t\t</DataAray>\n')

  # Write types

  # Write end of nodes
  meshFile.write('\t\t\t</Cells>\n')

def writeMeshData(mesh, meshFile):

  nNodes = mesh.nNodes
  nCells = mesh.nCells
  meshFile.write('\t\t<Piece NumberOfPoints="%i" NumberOfCells="%i">\n') % (nNodes, nCells)

  # Write nodes
  writeNodes(mesh, meshFile)

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
