"""
  compareFields:

    takes 2 data files and the name of a field e.g.

    results_data_0.h5
    results_data_1.h5
    /phase1/VFrac1

    and returns an array of the differences (normalised by the
    first reference field by default)

    arrDiff = (arrCom - arrRef) < OPTIONAL: / arrRef >
"""
import h5py
import numpy as np

def compareFields(fileRef, fileCom, field, norm = True):

  assert(isinstance(fileRef, str))
  assert(isinstance(fileCom, str))
  assert(isinstance(field, str))

  # Open data
  dataRef = h5py.File(fileRef, "r")
  dataCom = h5py.File(fileCom, "r")

  fieldRef = dataRef[field]
  fieldCom = dataCom[field]

  nEnt = len(fieldRef)
  assert(len(fieldCom) == nEnt)

  arrRef = np.zeros(nEnt)
  arrCom = np.zeros(nEnt)

  for i in range(nEnt):

    arrRef[i] = fieldRef[i][0]
    arrCom[i] = fieldCom[i][0]

  dataRef.close()
  dataCom.close()

  arrDiff = np.zeros(nEnt)
  for i in range(nEnt):

    arrDiff[i] = arrCom[i] - arrRef[i]

    if norm:

      arrDiff[i] /= arrRef[i]

  return arrDiff
