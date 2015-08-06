import h5py

def readData(dataFile = None, dataFields = None, phases = -1):

  assert(isinstance(dataFile, str))

  if isinstance(dataFields, str):

    nDataFields = 1

  else:

    nDataFields = len(dataFields)
    assert(nDataFields == len(phases))

  # Open dataFile
  hdf5File = h5py.File(dataFile, "r")

  # Read each field in dataFields
  data = {}
  for d in range(nDataFields):

    if nDataFields == 1 and isinstance(dataFields, str):

      fieldName = dataFields

    else:

      fieldName = dataFields[d]

    assert(isinstance(fieldName, str))

    if not isinstance(phases, int):

      phase = phases[d]

    else:

      phase = phases

    assert(isinstance(phase, int))

    # Check dataField exists
    name, group, nPhases = checkDataFieldExists(hdf5File, fieldName, phase)

    if nPhases:

      data[fieldName] = []
      for phase in range(nPhases):

        data[fieldName].append(None)
        data[fieldName][phase] = getDataField(hdf5File[group[phase]][name[phase]])

    else:

      if len(group):

        data[fieldName] = getDataField(hdf5File[group[0]][name[0]])

      else:

        data[fieldName] = getDataField(hdf5File[name[0]])

  # Close dataFile
  hdf5File.close()

  return data

def checkDataFieldExists(hdf5File, fieldName, phase):

  name = []
  groupKey = []
  nPhases = 0

  if fieldName in hdf5File.keys():

    # Field does not belong to a phase eg /Pressure
    name.append(fieldName)

  elif phase >= 0:

    # Phase number is specified - look for under /phase%i
    # eg /phase0/UVelocity0
    group = "phase" + str(phase)
    if group in hdf5File.keys():

      groupKey.append(group)
      name.append(fieldName + str(phase))

    else:

      # Error!
      pass

  else:

    # Phase number < 0 - look for all occurrences of field
    # eg /phase0/UVelocity0 AND /phase1/UVelocity1
    group = "phase"
    phase = 0
    while (group + str(phase)) in hdf5File.keys():

      nPhases += 1
      phaseGroup = group + str(phase)
      groupKey.append(phaseGroup)

      name.append(None)
      if (fieldName + str(phase)) in hdf5File[phaseGroup].keys():
        
        name[phase] = fieldName + str(phase)

      else:

        # Warning
        print "Could not find %s in %s" % (fieldName, phaseGroup)
        pass

      phase += 1

  return name, groupKey, nPhases

def getDataField(hdf5DataField):

  nPoints = len(hdf5DataField)
  data = [0] * nPoints
  for i in range(nPoints):

    data[i] = hdf5DataField[i][0]

  return data
