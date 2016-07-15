# S. Pickard
# June 2016
# (Using python 3.4.4, and brian2 2.0rc)
#
# DESCRIPTION



import numpy as np
from spikeMonToMatrix import spikeMon_To_Matrix
import pickle
import matplotlib.pyplot as plt

########################################################################################################################
# TESTING spike monitoring data to matrix
########################################################################################################################


# # In the second test we will load some data that we have created in simulation and see what it looks like
# # Input spike times
inputFile = open("savedData_0/netOutput0_PoiNeu_SpikesTimes.pkl","rb")
spikeTimes = pickle.load(inputFile)
spikeTimesUnits = pickle.load(inputFile)
inputFile.close()
# print (spikeTimes)

# Input spike times indices,
inputFile = open("savedData_0/netOutput0_PoiNeu_SpikesInds.pkl","rb")
spikeTimeInds = pickle.load(inputFile)
inputFile.close()
# print (spikeTimeInds)




NeurFire = spikeMon_To_Matrix(spikeTimeArray = spikeTimes, NeurIndexArray = spikeTimeInds)
NeurFire = np.array(NeurFire)
# nSpike = len(spikeCount)
# nTime = time_len = (len(time))
# print (nTime)
#
# nump_hist = plt.figure()
# plt.hist(spikeCount, bins = time)
# plt.figure(1)
# plt.hist(spikeCount, bins=50)
# # plt.bar(left, height = spikeCount, width = 1, facecolor = 'blue')
# plt.title("Spike Count Across Time Intervals")
# plt.xlabel("Time Intervals")
# plt.ylabel("Spike Count")
# # plt.axis([0,50])
# plt.grid(True)
# plt.show()
