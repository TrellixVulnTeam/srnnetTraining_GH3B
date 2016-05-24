# A. Lonsberry
# May 2016
# (Using python 3.4.4, and brian2 2.0rc)
#
# DESCRIPTION
#   Creating data, this will simply create data and save (using pickle) from a simple network.
#
# NETWORK DESCRIPTION
#   -Mostly taken from Carlson et al. "ramp" example (2013), some differences and addtions are made to equations
#   -100 input Poisson neurons
#   -1 RS Izhicevhich neuron
#   -STDP + Homeostatis (Carlson 2013) with some slight adaptations and alterations
#
# RECORDING DATA
#
from brian2 import *
import pickle
import numpy

########################################################################################################################
# Setting up Simultation Comilation
########################################################################################################################
# (brian2's 'standalone' compilation option is fast, thus we want to compile into c++ before running

# Nothing fancey where, we want to build on 'run'
set_device('cpp_standalone', directory='compiledCppSim')

########################################################################################################################
# Setting up General Simultation
########################################################################################################################

start_scope()
defaultclock.dt = 100. * usecond

########################################################################################################################
# Setting up Izh. Neuron Model(s)
########################################################################################################################

# With vlaues for (RS) type neuron used.
a = .02
b = .2
c = -65.0
d = 8.0

# I need time-constant values
tau1 = 1000 * ms
tau2 = 250 * ms

# Neuron dynamics
nurEqs = """
dv/dt = (0.04 * (v**2) + 5*v + 140 - u + I + 5*L)/tau1 : 1 (unless refractory)
du/dt = (a * ( b * v - u ) ) / tau1 : 1
dL/dt = -L/tau2 : 1
I : 1
"""
resetEqs = """
v = c
u = u + d
"""

# Make Neuron Group 1, where we have the single output Izh. type neuron of "RS" type
G = NeuronGroup(1, model=nurEqs, threshold='v > 30.', reset=resetEqs, refractory=2 * ms, method='euler')

########################################################################################################################
# Setting up Poisson Neurons
########################################################################################################################

P = PoissonGroup(100, numpy.arange(100) * .2 * Hz + .2 * Hz)

########################################################################################################################
# STDP + Homeostatis Synapses (Carlson 2013)
########################################################################################################################

# Synapse constants and parameters, mostly like those in (Carlson 2013)
taupre  = .020 * second
taupost = .060 * second
Apre    = .0002
Apost   = -.000066
R_tar   = 6.6425  # This value is calculated for the low-pass filter and using 10Hz
tauR    = 1 * second
beta    = 1
alpha   = .4
gamma   = 50
T       = 5

#Synapse dynamics and models
S = Synapses(P, G, model="""
                         dw/dt = (alpha * w * (1 - R_hat / R_tar) * K) / (1*second)  : 1 (clock-driven)
                         dapre/dt = -apre / taupre : 1 (event-driven)
                         dapost/dt = -apost / taupost : 1 (event-driven)
                         dR_hat/dt = -R_hat/tauR : 1 (clock-driven)
                         K = R_hat / ( T * abs( 1 - R_hat / R_tar) * gamma) : 1
                         """,
             on_pre="""
                         L += w
                         apre += Apre
                         w += beta * K * apost
                         """,
             on_post="""
                         apost += Apost
                         w += beta * K * apre
                         R_hat += 1
                         """,
             method='euler')

# Connect all neurons in group 'P' to group 'G'
S.connect()

# Set the weights equivelently
S.w = 2.0

########################################################################################################################
# Monitors
########################################################################################################################

# I will make the recording operate at a different rate by changing the time-step in the monitor (change "dt" value)
SynMonitor  = StateMonitor(S, ['w', 'R_hat', 'K'], record=numpy.arange(100), dt=.500*ms)
PoiMonitor  = SpikeMonitor(P)
NeuMonitor1 = SpikeMonitor(G)
NeuMonitor2 = StateMonitor(G, ['v', 'u', 'L'], record=0, dt=.500*ms)

########################################################################################################################
# RUN
########################################################################################################################

run(50*second)

########################################################################################################################
# Save
########################################################################################################################
# Now we want to save our results with the pickle function, IMPORTANTALY, brian has all these units floating around, we
# need to get rid of them to use the pickle stuff, thus you will see things like "...numpy.asarray()..." to recast
# and get rid of the units. (See brian2 online docs, http://brian2.readthedocs.io/en/2.0rc1/user/units.html)

#print("The type for SynMonitor.t is: ",type(SynMonitor.t))
#print("The type for NeuMonitor1.t is: ",type(NeuMonitor1.t))
#print("The type for SynMonitor.t[0] is: ",type(SynMonitor.t[0]))
#print("The type for SynMonitor.w is: ",type(SynMonitor.w))
#print("The type for NeuMonitor1.t is: ",type(NeuMonitor1.t))
print("NeuMonitor1.t is \n", NeuMonitor1.t)
print("SynMonitor.t is \n", SynMonitor.t)
#print("The type for numpy.asarry(NeuMonitor1.t) is: ", type(numpy.asarray(NeuMonitor1.t)))

outputFile = open("netOutput0_Syn_t.pkl","wb")
pickle.dump(SynMonitor.w, outputFile)
outputFile.close()

outputFile = open("netOutput0_Syn_w.pkl","wb")
pickle.dump(numpy.asarray(SynMonitor.t), outputFile)
outputFile.close()

outputFile = open("netOutput0_Syn_Rhat.pkl","wb")
pickle.dump(SynMonitor.R_hat, outputFile)
outputFile.close()

outputFile = open("netOutput0_Syn_K.pkl","wb")
pickle.dump(SynMonitor.K, outputFile)
outputFile.close()

outputFile = open("netOutput0_Neu_v.pkl","wb")
pickle.dump(NeuMonitor2.v, outputFile)
outputFile.close()

outputFile = open("netOutput0_Neu_u.pkl","wb")
pickle.dump(NeuMonitor2.u, outputFile)
outputFile.close()

outputFile = open("netOutput0_Neu_v.pkl","wb")
pickle.dump(NeuMonitor2.L, outputFile)
outputFile.close()

outputFile = open("netOutput0_PoiNeu_SpikesTimes.pkl","wb")
pickle.dump(numpy.asarray(PoiMonitor.t), outputFile)
outputFile.close()

outputFile = open("netOutput0_PoiNeu_SpikesInds.pkl","wb")
pickle.dump(PoiMonitor.i, outputFile)
outputFile.close()

outputFile = open("netOutput0_Neu_SpikesTimes.pkl","wb")
pickle.dump(numpy.asarray(NeuMonitor1.t), outputFile)
outputFile.close()

outputFile = open("netOutput0_Neu_SpikesInds.pkl","wb")
pickle.dump(NeuMonitor1.i, outputFile)
outputFile.close()

