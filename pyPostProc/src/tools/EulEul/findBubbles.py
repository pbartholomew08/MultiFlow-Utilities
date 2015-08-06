"""
  findBubbles.py:

    Provides method to find bubbles in a Volume-fraction field
"""
def findBubbles(mesh, VFrac, cutoff = 0.6):

  nBubbles = 0
  bubbles = []

  nCells = mesh.nCells
  for cell in range(nCells):

    if VFrac[cell] >= cutoff:

      # See if attached to a bubble
      for b in range(nBubbles):
        for nb in mesh.cells[c].neighbours:

          if nb in bubbles[b]:

            bubbles[b].append(cell)

          else:

            bubbles.append([cell])
            nBubbles += 1

        # Merge bubbles
