"""
  writeHDF5Mesh:

    writes out mesh in MultiFlow-Unstructured HDF5 format
"""
import h5py

def writeMeshData(mesh, meshFile):

  # Create dataset
  arr = [0] * 7
  meshFile.create_dataset("meshData", arr)

def writeHDF5Nodes(mesh, meshFile):

  nNodes = mesh.nNodes

def writeHDF5Cells(mesh, meshFile):

  nCells = mesh.nCells

def writeHDF5Faces(mesh, meshFile):

  nFaces = mesh.nFaces

def writeHDF5Mesh(mesh, filePath, fileName):

  # Open file
  meshFile = h5py.File(filePath + fileName, "r")

  # Write meshData
  writeMeshData(mesh, meshFile)

  # Write nodes
  writeHDF5Nodes(mesh, meshFile)

  # Write cells
  writeHDF5Cells(mesh, meshFile)
  
  # Write faces
  writeHDF5Faces(mesh, meshFile)

  # Close file
  meshFile.close()
