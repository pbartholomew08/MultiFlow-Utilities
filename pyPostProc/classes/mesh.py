"""
  mesh classes:
  
    node:
    face:
    cell:
    mesh:
"""
import math
import numpy as np

# node class
class node(object):
  """
    Node class: represents a 3-dimensional point\n
    Members:
      node.X:       numpy array of length 3 to hold coordinates\n
      node.bndFlg:  integer representing if on boundary\n
      node.ID:      integer giving node's index\n
    Methods:
  """  

  # Initialisation
  def __init__(self, x = 0.0, y = 0.0, z = 0.0, idx = -1):
    
    self.X = np.zeros(3)

    self.X[0] = x
    self.X[1] = y
    self.X[2] = z
    
    assert(isinstance(idx, int))
    self.idx = idx

  def setIndex(self, idx):

    assert(isinstance(idx, int))
    self.idx = idx
    
# face class
class face(object):
  """
    class face:
    
      X:        face centre coordinates
      norm:     normal vector
      area:     face area
      bndType:  Integer boundary type flag
      nodes:    List of nodes making up face
      cells:    List of faces either side of face
      
      methods:
      
        getNorm():    operates on self, determines and sets normal vector
        getArea():    operates on self, determines and sets area
        orderNodes(): operates on self, puts nodes in clockwise order
        orderCells(): operates on self, puts cells in lower-higher order
  """
  
  # Initialisation
  def __init__(self, nodes, idx = -1):
    
    # Setup arrays
    self.X = np.zeros(3)
    self.norm = np.zeros(3)
    
    self.node = []
    self.cell = []
    self.nCells = 0
    
    self.nNodes = len(nodes)
    assert(self.nNodes > 2)

    for n in range(self.nNodes):
      
      self.node.append(nodes[n].idx)
      
    self.calcCentre(nodes)
    self.orderNodes(nodes)
    self.calcNorm(nodes)
    self.calcArea(nodes)
    
    assert(isinstance(idx, int))
    self.idx = idx
    self.bndFlg = 0
      
  # Compute centre
  def calcCentre(self, nodes):
    
    for i in range(3):
      for n in range(self.nNodes):
        
        self.X[i] += nodes[n].X[i]
      
      self.X[i] /= self.nNodes
      
  # Order nodes to be anti-clockwise when looking down norm
  def orderNodes(self, nodes):
    
    ordered = False
    nodeArr = range(self.nNodes)
    e = np.ones(3)
    
    while not ordered:
      
      for i in range(1, self.nNodes - 1):
        
        v1 = nodes[nodeArr[i]].X - nodes[0].X
        v2 = nodes[nodeArr[i + 1]].X - nodes[0].X
        
        cross = np.cross(v1, v2)
        dot = (cross * e).sum()
        if dot < 0.0:

          nodeArr[i], nodeArr[i + 1] = nodeArr[i + 1], nodeArr[i]
          
      fixed = True
      for i in range(1, self.nNodes - 1):
        
        v1 = nodes[nodeArr[i]].X - nodes[0].X
        v2 = nodes[nodeArr[i + 1]].X - nodes[0].X
        
        cross = np.cross(v1, v2)
        dot = (cross * e).sum()
        if dot < 0.0:
          
          fixed = False
          break
          
      ordered = fixed
      
    self.node = [self.node[nodeArr[i]] for i in range(self.nNodes)]
      
  # Compute norm
  def calcNorm(self, nodes):
    
    v1 = nodes[1].X - nodes[0].X
    v2 = nodes[2].X - nodes[0].X
    
    self.norm = np.cross(v1, v2)
    self.norm /= math.sqrt((self.norm**2).sum())
    
  # Compute area
  def calcArea(self, nodes):
    
    self.area = 0.0
    
    for n in range(1, self.nNodes - 1):
      
      v1 = nodes[n].X - nodes[0].X
      v2 = nodes[n + 1].X - nodes[0].X
      
      self.area += 0.5 * (((np.cross(v1, v2)**2).sum())**0.5)
      
  # Link cell
  def linkCell(self, cellIdx):
    
    assert(isinstance(cellIdx, int))
    self.cell.append(cellIdx)
    self.nCells += 1
    
# cell class
"""
  class cell:
  
    X:        cell-centre
    volume:   volume of cell
    bndFlg:   indicates if any of faces are boundary faces
    faces:    list of faces defining cell
    normSign: list indicating whether face points away from or towards cell centre
    aVec:     list of vectors from cell to face centres
    
    methods:
    
      getCentre():    operates on self, determines and sets cell centre
      getNormSigns(): operates on self, determines and sets normSigns
      getaVec():      operates on self, determines and sets aVecs
      getVol():       operates on self, determines and sets volume
"""
class cell(object):
  
  # Initialisation
  def __init__(self, nodes, idx = -1):
    
    # Setup arrays
    self.X = np.zeros(3)
    
    self.node = []
    self.face = []
    self.nFaces = 0

    self.neighbour = []
    self.nNeighbours = 0

    self.nNodes = len(nodes)
    assert(self.nNodes > 3)
    for n in range(self.nNodes):
      
      self.node.append(nodes[n].idx)
      
    self.calcCentre(nodes)
    
    assert(isinstance(idx, int))
    self.idx = idx
      
  # Calculate centre
  def calcCentre(self, nodes):
    
    for i in range(3):
      for n in range(self.nNodes):
        
        self.X[i] += nodes[n].X[i]
        
      self.X[i] /= self.nNodes
      
  # Calculate normSign
  def calcNormSign(self, faces):
    
    for f in range(self.nFaces):
      
      a = faces[f].X - self.X
      
      dot = (a * faces[f].norm).sum()
      if dot > 0.0:
        
        self.normSign[f] = 1.0
        
      else:
        
        self.normSign[f] = -1.0
        
  # Calculate volume
  def calcVolume(self, nodes, faces):
  
    self.vol = 0.0

    ONE_THIRD = 1.0 / 3.0
 
    for f in range(self.nFaces):
      j = self.face[f]
      # Compute volume of tetrahedra who's bases makeup the face and share the centre as one of their vertices
      n0 = nodes[faces[j].node[0]]       
      n1 = nodes[faces[j].node[1]]
      n2 = nodes[faces[j].node[2]]

      a = n0.X - self.X
      b = n1.X - self.X
      c = n2.X - self.X

      self.vol += ONE_THIRD * abs(np.dot(a, np.cross(b, c)))
        
  # Link face
  def linkFace(self, faceIdx):
    
    self.face.append(faceIdx)
    self.nFaces += 1

  # Link neighbour
  def linkNeighbour(self, cellIdx):

    self.neighbour.append(cellIdx)
    self.nNeighbours += 1
    
# mesh class
class mesh():
  
  def __init__(self, nodes, faces, cells):
    
    self.nodes = nodes
    self.faces = faces
    self.cells = cells
    self.nBoundaries = 0
    
    self.nNodes = len(nodes)
    self.nFaces = len(faces)
    self.nCells = len(cells)

    bndTypes = []
    for f in range(self.nFaces):
      
      bndFlg = self.faces[f].bndFlg
      if bndFlg and not (bndFlg in bndTypes):

        bndTypes.append(bndFlg)
        self.nBoundaries += 1
