import h5py
import numpy as np

def getAvgVFracDist(filePath, fileName, t0, tEnd, phase=0, nBins = 100, r = (0, 1), dens = True, quiet = True):

  assert(isinstance(t0, int))
  assert(isinstance(tEnd, int))
  assert(isinstance(phase, int))
  assert(isinstance(filePath, str))
  assert(isinstance(fileName, str))
  assert(isinstance(nBins, int))
  assert(isinstance(r, tuple))

  VFracDist = [0] * nBins
  VFracRange = [0] * nBins
  for i in range(nBins):

    VFracRange[i] = r[0] + i * (r[1] - r[0]) / float(nBins)

  # Load data
  N = tEnd - t0
  for n in range(t0, tEnd):

    f = filePath + "/" + fileName + str(n) + ".h5"
    if not quiet:
      print f
    data = h5py.File(f, "r")
    VFracData = data["/phase" + str(phase) + "/VFrac" + str(phase)]
    nCells = len(VFracData)
    VFrac = [0] * nCells
    for i in range(nCells):

      VFrac[i] = VFracData[i][0]

    data.close()

    # Compute histogram
    hist, bin_edge = np.histogram(VFrac, nBins, range = r, density = dens)
    for b in range(nBins):

      VFracDist[b] += hist[b] / float(N)

  return VFracDist, VFracRange

