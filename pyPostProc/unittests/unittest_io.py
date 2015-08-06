import unittest
import os
from pyPostProc.src.io.readMesh import readHDF5Mesh as readHDF5Mesh

class unittest_readMesh(unittest.TestCase):

  def setUp(self):

    if os.getcwd() == os.path.dirname(os.path.realpath(__file__)):
      self.fileName = "./mesh_10x10x10.h5"
    else:
      self.fileName = "./unittests/mesh_10x10x10.h5"

    N = 10
    L = 1.0

    self.expected_nNodes = (N + 1)**3
    self.expected_nCells = N**3
    self.expected_nFaces = 3 * (N + 1) * (N**2)

    dx = float(N) / L

    self.node_xRange = [0] * (N + 1)
    for i in range(N + 1):

      self.node_xRange[i] = i * dx

  def tearDown(self):

    pass

  def test_readHDF5Mesh(self):

    self.mesh = readHDF5Mesh(self.fileName, True)

    nNodes = self.mesh.nNodes
    nCells = self.mesh.nCells
    nFaces = self.mesh.nFaces

    self.assertEqual(nNodes, self.expected_nNodes)
    self.assertEqual(nCells, self.expected_nCells)
    self.assertEqual(nFaces, self.expected_nFaces)

#    for i in range(nNodes):
#      
#      X = self.mesh.nodes[i].X
#      for dim in range(3):
#
#        self.assertTrue(X[dim] in self.node_xRange)

def runTests():

  unittest.main()

if __name__ == "__main__":

  runTests()
