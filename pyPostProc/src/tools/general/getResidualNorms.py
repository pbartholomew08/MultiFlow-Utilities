import matplotlib.pyplot as plt

"""
  getResidualNorms:
    
    Reads the residual norm file and returns for a given timestep:

      ([EqNorms[]], systemNorm[])

    where EqNorms[] are the norms for each sub equation
    systemNorm is the norm for the coupled system
"""
def getResidualNorms(filePath, fileName, time, normalise = True):

  with open(filePath + fileName, "r") as resFile:

    line = resFile.readline()
    nEq = len(line.split()) - 2

    eqNorms = []
    for eq in range(nEq):
      eqNorms.append([])

    sysNorm = []

    # Read file
    while line:

      data = line.split()
      timeStep = float(data[0])
      if timeStep == time:

        for eq in range(nEq):

          eqNorms[eq].append(float(data[1 + eq]))

        sysNorm.append(float(data[1 + nEq]))

      line = resFile.readline()

  if normalise:

    for eq in range(nEq):

      norm0 = eqNorms[eq][0]

      for i in range(len(eqNorms[eq])):

        eqNorms[eq][i] /= norm0

    norm0 = sysNorm[0]
    for i in range(len(sysNorm)):

      sysNorm[i] /= norm0

  return eqNorms, sysNorm

"""
  plotResidualNorms

    plots the equation and system norms returned by getResidualNorms
"""
def plotResidualNorms(filePath, fileName, time, normalise = True):

  eqNorms, sysNorm = getResidualNorms(filePath, fileName, time, normalise)

  nEq = len(eqNorms)
  for eq in range(nEq):

    plt.plot(eqNorms[eq], label = "Equation " + str(eq))

  plt.plot(sysNorm, label = "System")

  # Format plot
  plt.legend()
  plt.yscale("log")
  plt.xlabel("Iteration")
  plt.grid()
  if normalise:

    plt.ylabel("Normalised Value")

  plt.show()
