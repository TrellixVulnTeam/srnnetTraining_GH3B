# A.Lonsberry
# October 2016
#
# DESCRIPTION
#   Here I am going to have methods to create and save data for this experiment. The methods below are VERY hardcoded,
#   but rely on other methods that are generic. They are hardcoded so we can generate very specific data (original data,
#   decomposed original data, and then spiking from analog)

import matplotlib.pyplot as plt

# I had a difficult time getting things to import, so now I have however, go about fixing this by going up a directoy
# which I think I can do in the following way.
import os
import sys
import pickle
sys.path.append(os.path.abspath("../"))

# Call the python file that has the 1D mass simulator in it.
from dataGenerators import movingPointMass1D
from spikeDataGenerators import decompDimensions

########################################################################################################################
# METHODS FOR CREATING 1D MOVING MASS DATA (SMOOTH, DECOMPOSED, SPIKING)
########################################################################################################################

def genAndSaveMoving1DMassData(saveName='movingPointMassData/pointMassData000.pkl'):
    """
    DESCRIPTION
    Here we call the methods repeatedly to make instances of the 1D moving mass. Of these n examples, we then put them
    into a list, and then save them in the appropriate folder.
    :return: N/A (we save data to a file), the list saved is [listOfTrials, xmin, xmax, vmin, vmax, amin, amax, dt, tmax]
    """
    #How many iterations we want to include
    Iterations = 10
    xmin = 0.0
    xmax = 5.0
    vmin = 1.0
    vmax = 5.0
    amin = 1.0
    amax = 2.0
    dt   = .001
    tmax = 10.0
    dataOut = []
    for i in range(Iterations):
        funcOuts = movingPointMass1D.randomMassMovement(xmin, xmax, vmin, vmax, amin, amax, dt, tmax)
        dataOut.append(funcOuts)
    toSave = [dataOut, xmin, xmax, vmin, vmax, amin, amax, dt, tmax]
    outputFile = open(saveName, "wb")
    pickle.dump(toSave,outputFile)
    outputFile.close()

def decomposeMoving1DMassData(dataFile='movingPointMassData/pointMassData000.pkl', saveName='movingPointMassData/pointMassDataDecmp000.pkl' ):
    """
    DESCRIPTION
    This is made to take 1D point mass trails, given the file name is given, and then subseqently make normal functions
    to decompose the original 1D doamin, and then actually decompose the domain, and then save the results
    :param dataFile: string, the location where we have the data stored
    :param saveName: string, the location where we want to save the results
    :return: N/A (we save data to a file), the list saved is [list of segmented 1D trails (numpy.arrays), gCenters (
            numpy.array), b (scalar), file name of original data (string)]
    """
    # Load in the saved 1D moving mass. Inside the loaded list of lists, we will have a list that has a bunch of
    # seperate 1D numpy.arrays that represent the position of the mass through different random trials.
    inputFile = open(dataFile, "rb")
    trackingData = pickle.load(inputFile)
    inputFile.close()
    trackedArrays = trackingData[0]
    print(len(trackedArrays))

    # Now we need to generate the Gaussians functions that will be used to decompose the 1D data into seperete parts
    # that will represent inputs from individual neurons.
    xStart = 0.0
    xStop = 5.0
    nGaus = 10
    bInitial = .05
    dt = 0.001
    cfds = decompDimensions.minVarOverlappingGaussian(xStart, xStop, nGaus, bInitial, dt)
    gCenters = cfds[0]
    b = cfds[1]

    # Now we need to parse the loaded data with the generated Gaussians
    #seperateInputValuesAlongGaussians(trackingData, gcenters, b, normalize=False)
    segmentedTrials = [] #This is where we will put the decomposed 1D mass trials.
    for i in range(len(trackedArrays)):
        decomped = decompDimensions.seperateInputValuesAlongGaussians(trackedArrays[i][0], gCenters, b)
        segmentedTrials.append(decomped)

    # Now we want to save the decomposed 1D arrays and the Gaussians that made them, and also cite the original
    # data that was used.
    toSave = [segmentedTrials, gCenters, b, dataFile]
    outputFile = open(saveName, "wb")
    pickle.dump(toSave, outputFile)
    outputFile.close()




########################################################################################################################
# RUNNING METHODS
########################################################################################################################

if __name__ == "__main__":

    # Create and save some data
    #generateAndSaveMoving1DMassData()
    # Load the data back
    #inputFile = open("movingPointMassData/pointMassData000.pkl", "rb")
    #dataOut = pickle.load(inputFile)
    #inputFile.close()
    #for i in range(len(dataOut[0])):
    #    plt.figure(i)
    #    plt.plot(dataOut[0][i][1],dataOut[0][i][0])
    #plt.show()

    #
    decomposeMoving1DMassData()