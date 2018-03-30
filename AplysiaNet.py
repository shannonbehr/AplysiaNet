from Interface import Interface
from Neuron import Neuron
from Synapse import Synapse
from tkinter import *
import csv

class AplysiaNet:

    def __init__(self):
        # Initializes the interface and runs it until the user enters valid inputs and clicks "run."
        root = Tk()
        interface = Interface(root)
        while interface.get_status() == 'running':
            root.update()

        # The input from the interface is stored here
        self.input = interface.get_input()

        # The model is set up to run for 8.5 seconds
        self.duration = 8.5

        # The frequency will be evaluated every 0.000008 seconds
        self.step_size = 0.000008

        # The model starts at time = 0 seconds
        self.time = 0

        # The default value for current is 10
        self.current = 10

        # This will store the neurons in the circuit
        self.neurons = []

        # This will store the synapses in the circuit
        self.synapses = []

        self.neurons_to_output = []

        self.outputs = []

    def set_neurons(self, neurons):
        self.neurons = neurons

    def set_synapses(self, synapses):
        self.synapses = synapses

    def set_neurons_to_output(self, neurons_to_output):
        self.neurons_to_output = neurons_to_output

    def run(self):
        # Creates a .csv file for the data; TODO: file writing!
        data_file = open('AplysiaData.csv', 'w')
        writer = csv.writer(data_file, dialect='excel-tab')

        # At each time step, update each neuron and run the output through the synapses to become the next inputs
        for index in range(0, (int)((1 / self.step_size)*(self.duration))):
            for neuron in self.neurons:
                neuron.update(self.time, neuron.get_next_current(self.time))

            for synapse in synapses:
                synapse.update(self.time)
            self.time += self.step_size

        # This is for testing purposes; print the output of each neuron
        for neuron in self.neurons_to_output:
            self.selective_print(neuron.get_output())
            self.outputs.append(neuron.get_output())
            # This worked a bit better than the current file writing system but isn't the right approach since I made the list nested:
            #for val in neuron.get_output():
                #writer.writerow([val])

        # This doesn't work very well. There is too much data, and there seems to be a column limit in place, so things
        # are not formatting correctly. It's also slowing things down significantly. I will see what I can cut out to pass
        # into the biokinetic model.
        writer.writerows(self.outputs)

        data_file.close()

    # Generates an array of chemical or mechanical input to a neuron given stimulus start and end times
    def handle_inputs(self, start, end, storage):
        for index in range(0, (int)((1 / self.step_size)*(self.duration))):
            if index*self.step_size < start or index*self.step_size > end:
                storage[index] = 0
            else:
                storage[index] = self.current

    # Prints out an array of every 0.25 seconds; this is for testing purposes
    def selective_print(self, arr):
        arr_str = []
        index = 0
        while index < len(arr):
            arr_str.append(arr[index])
            index = index + int(0.25 / self.step_size)
        print(arr_str)

# Creates the network.
network = AplysiaNet()

# This code gets the input from the user and translates into an input array for the network.
inputs = network.input
chem_input = []
mech_input = []
neuron2_input = []
for i in range (0, (int)((1 / network.step_size)*(network.duration))):
    chem_input.append(0)
    mech_input.append(0)
    neuron2_input.append(0)
network.handle_inputs(inputs[0], inputs[1], chem_input)
network.handle_inputs(inputs[2], inputs[3], mech_input)

# This code builds the circuit. For now, it is a test circuit with two typical IK neurons and a single excitatory* synapse.
# * the synapse hyperpolarizes too much. It should be excitatory with these params, but is mildly inhibitory instead.
neuron1 = Neuron(0.006, 0.25, -65, 8, chem_input, 0.000008, 0)
neuron2 = Neuron(0.006, 0.25, -65, 8, neuron2_input, 0.000008, 0)
synapse = Synapse(neuron1, neuron2, 5, 10, 75, 0.000008, 0)
neurons = [neuron1, neuron2]
synapses = [synapse]

# The neurons and synapses are given to the network, and the simulation runs.
network.set_neurons(neurons)
network.set_synapses(synapses)
network.set_neurons_to_output(neurons)
network.run()

#TODO
#figure out why synapse parameters aren't generating expected behavior
#sanity checks