

from pyNN.random import RandomDistribution, NumpyRNG
import pyNN.neuron as sim
from pyNN.utility import get_script_args, Timer, ProgressBar, init_logging, normalized_filename
from auxRoutines import *


simTimeIni = 0
simTimeFin = 1000
timeBoundKernel = 400
timeStep = 0.1


sim.setup(timestep=timeStep, min_delay=0.5)


weightInhibToInhibSynapses = 0.03 	# [uS]






tau_m 		= 20.0	# [ms]
cm 		= 0.2 	# [nF]
v_rest 		= -60.0	# [mV]
v_thresh 	= -50.0 # [mV]
tau_syn_E 	= 5.0	# [ms]
tau_syn_I 	= 10.0	# [ms]
e_rev_E 	= 0.0	# [mV]
e_rev_I 	= -80.0	# [mV]
v_reset 	= -60.0	# [mV]
tau_refrac 	= 5.0	# [ms]
i_offset 	= 0.0	# [nA]

eta = 1e-4
eta = weightInhibToInhibSynapses * eta  # weight of inhibitory to excitatory synapses
rho = 0.003

synapseDelay = 0.5 # [ms]


neuronParameters = 	{
			'tau_m':	tau_m,	
			'cm':		cm, 	
			'v_rest':	v_rest,	
			'v_thresh':	v_thresh, 	
			'tau_syn_E':	tau_syn_E,	
			'tau_syn_I':	tau_syn_I,	
			'e_rev_E':	e_rev_E,	
			'e_rev_I':	e_rev_I,	
			'v_reset':	v_reset,	
			'tau_refrac':	tau_refrac,	
			'i_offset': 	i_offset	
			}


cell_type = sim.IF_cond_exp(**neuronParameters)

input = sim.Population(20, sim.SpikeSourcePoisson(rate=50.0))
output = sim.Population(25, cell_type)




rand_distr = RandomDistribution('uniform', (v_reset, v_thresh), rng=NumpyRNG(seed=85524))

output.initialize(v=rand_distr)



stdp = sim.STDPMechanism(weight_dependence=sim.AdditiveWeightDependence(w_min=0.0, w_max=0.1),
                         timing_dependence=sim.Vogels2011Rule(eta=0.0, rho=1e-3),
                         weight=0.005, delay=0.5)





fpc 	= sim.FixedProbabilityConnector(0.02, rng=NumpyRNG(seed=854))



connections = sim.Projection(input, output, fpc,
                             synapse_type=stdp,
                             receptor_type='excitatory')


connections.set(eta=0.0003)


output.record(['spikes', 'v'])

sim.run(simTimeFin - simTimeIni)


print("\n\nETA: input to output:")
print connections.get('eta', format='list')


print("\n\ninput to output:")
print connections.get('weight', format='list')




data = output.get_data().segments[0]

popSpikes = output.get_data('spikes')

numNeuronsPop = 20
numNeuronsPop2 = 15

sampledPop = output.sample(numNeuronsPop, rng=NumpyRNG(seed=85524))
sampledPopSpikes = sampledPop.get_data('spikes')

sampledPop2 = output.sample(numNeuronsPop2, rng=NumpyRNG(seed=8527))
sampledPopSpikes2 = sampledPop2.get_data('spikes', clear="true")



#sim.end()

import matplotlib.pyplot as plt


plt.figure(1)

vm = data.filter(name='v')[0]
for signal in vm.T:
    plt.plot(signal.times, signal)
plt.xlabel("Time (ms)")
plt.ylabel("Vm (mV)")

fig = plt.figure(2)
plotRaster2(popSpikes, 'red')



fig3 = plt.figure(3)
plotSpikeTrains(popSpikes, timeStep, simTimeIni, simTimeFin)


fig4 = plt.figure(4)
y = biExponentialKernel (timeStep, timeBoundKernel)
x = np.linspace(-timeBoundKernel, timeBoundKernel, num = int(2*timeBoundKernel/timeStep) + 1)
plt.plot(x, y)




fig6 = plt.figure(6)

ax6_1 = fig6.add_subplot(2, 1, 1)
plotFilteredSpikeTrains(sampledPopSpikes, timeStep, simTimeIni, simTimeFin, timeBoundKernel)

plt.ylabel('Filtered spike trains')
plt.xlabel('Time [ms]')


ax6_2 = fig6.add_subplot(2, 1, 2)


plotCorrHist(ax6_2, numNeuronsPop, sampledPopSpikes, timeStep, simTimeIni, simTimeFin, timeBoundKernel, 'r')
'''

fig7 = plt.figure(7)
ax7 = fig7.add_subplot(2, 1, 2)
plotCorrDoubleHist(ax7, numNeuronsPop, sampledPopSpikes, 'red', numNeuronsPop2, sampledPopSpikes2, 'black', timeStep, simTimeIni, simTimeFin, timeBoundKernel)


sim.run(1000.0)


sampledPopSpikes = sampledPop.get_data('spikes')

sampledPopSpikes2 = sampledPop2.get_data('spikes', clear="true")


fig8 = plt.figure(8)
ax8 = fig8.add_subplot(2, 1, 2)
plotCorrDoubleHist(ax8, numNeuronsPop, sampledPopSpikes, 'red', numNeuronsPop2, sampledPopSpikes2, 'black', timeStep, simTimeFin, 2000, timeBoundKernel)
'''

plt.show()














