from Interface import Interface
from Neuron import Neuron
from Synapse import Synapse
from tkinter import *

class AplysiaNet:

    def __init__(self):
        # Initializes the interface and runs it until the user enters valid inputs and clicks "run."
        root = Tk()
        interface = Interface(root)
        while interface.get_status() == 'running':
            root.update()

        # The input from the interface is stored here
        self.input = interface.get_input()

        # The step size value is that used by Greg Sutton; the same value was chosen here to integrate the two models.
        self.step_size = 0.000008

        # The model is set up to run for 8.5 seconds
        self.duration = 8.5

        # The frequency will be evaluated every 0.25 seconds
        self.period_length = 0.25

        # The model starts at time = 0 seconds
        self.time = 0

        # The default value for current is 10
        self.current = 10

        # This will store the neurons in the circuit
        self.neurons = []

        # This will store the synapses in the circuit
        self.synapses = []

    def set_neurons(self, neurons):
        self.neurons = neurons

    def set_synapses(self, synapses):
        self.synapses = synapses

    def run(self):
        # At each time step, update each neuron and run the output through the synapses to become the next inputs
        for index in range(0, (int)((1 / self.period_length)*(self.duration))):
            for neuron in self.neurons:
                neuron.update(self.time, neuron.get_next_current(self.time))
            for synapse in synapses:
                synapse.update(self.time)
            self.time += self.period_length

        # This is for testing purposes; print the output of each neuron
        for neuron in self.neurons:
            print(neuron.get_output())

    # Generates an array of chemical or mechanical input to a neuron given stimulus start and end times
    def handle_inputs(self, start, end, storage):
        for index in range(0, (int)((1 / self.period_length)*(self.duration))):
            if index*self.period_length < start or index*self.period_length > end:
                storage[index] = 0
            else:
                storage[index] = self.current

# Creates the network.
network = AplysiaNet()

# This code gets the input from the user and translates into an input array for the network.
inputs = network.input
chem_input = []
mech_input = []
neuron2_input = []
for i in range (0, 34): #Un-hard code this to accomodate different step sizes
    chem_input.append(0)
    mech_input.append(0)
    neuron2_input.append(0)
network.handle_inputs(inputs[0], inputs[1], chem_input)
network.handle_inputs(inputs[2], inputs[3], mech_input)

# This code builds the circuit. For now, it is a test circuit with two typical IK neurons and a single excitatory* synapse.
# * the synapse hyperpolarizes too much. It should be excitatory with these params, but is mildly inhibitory instead.
neuron1 = Neuron(0.006, 0.25, -65, 8, chem_input, 0.000008, 0.25, 0)
neuron2 = Neuron(0.006, 0.25, -65, 8, neuron2_input, 0.000008, 0.25, 0)
synapse = Synapse(neuron1, neuron2, 1, 10, 75, 0.25, 0)
neurons = [neuron1, neuron2]
synapses = [synapse]

# The neurons and synapses are given to the network, and the simulation runs.
network.set_neurons(neurons)
network.set_synapses(synapses)
network.run()

#TODO
#figure out why synapses are making things so negative
#figure out enough time steps - this means file writing. sigh.
#sanity checks
#undo frequency?