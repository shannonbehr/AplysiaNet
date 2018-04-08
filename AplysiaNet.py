from Interface import Interface
from Neuron import Neuron
from Synapse import Synapse
from tkinter import *
import csv
import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

class AplysiaNet:

    def __init__(self):
        # Initializes the interface and runs it until the user enters valid inputs and clicks "run."
        root = Tk()
        interface = Interface(root)
        while interface.get_status() == 'running':
            root.update()

        self.start_time = time.time()

        # The input from the interface is stored here
        self.input = interface.get_input()

        # The current from the user input is stored here
        self.current = interface.get_current()

        # The model is set up to run for 8.5 seconds
        self.duration = 8.5

        # The frequency will be evaluated every 0.000008 seconds
        self.step_size = 0.000008

        # The model starts at time = 0 seconds
        self.t = 0

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
        # Creates a .csv file for the data
        data_file = open('AplysiaData.csv', 'w')
        writer = csv.writer(data_file, lineterminator= '\n')

        # At each time step, update each neuron and run the output through the synapses to become the next inputs
        for index in range(0, (int)((1 / self.step_size)*(self.duration))):
            for neuron in self.neurons:
                neuron.update(self.t)

            for synapse in synapses:
                synapse.update(self.t)
            self.t += self.step_size

        # This is for testing purposes; print the output of each neuron
        for neuron in self.neurons_to_output:
            self.selective_print(neuron.get_output())
            self.outputs.append(neuron.get_output())

        # This handles the output data to be written
        int_arr = list(range((int)(8.5/0.000008)))
        self.time_arr = [i * 0.000008 for i in int_arr]

        output_arr = [self.time_arr] + self.outputs
        output_arr = zip(*output_arr)

        # This currently writes every 10th time step to a file.
        for i, val in enumerate(output_arr):
            if i % 10 == 0:
                writer.writerow(val)

        # Computes and prints the total run time of the simulation minus graphing
        end_time = time.time()
        total_time = end_time - self.start_time
        print('Total time = %s seconds' % total_time)

        self.graph()

        data_file.close()

    # Generates an array of chemical or mechanical input to a neuron given stimulus start and end times
    def handle_inputs(self, start, end, storage, type):
        if type == 'chem':
            current = self.current[0]
        elif type == 'mech':
            current = self.current[1]
        else:
            raise ValueError('Input type must be either chemical (chem) or mechanical (mech).')
        if start == end:
            return
        for index in range(0, (int)((1 / self.step_size)*(self.duration))):
            if index*self.step_size < start or index*self.step_size > end:
                storage[index] = 0
            else:
                storage[index] = current

    # Prints out an array of every 0.25 seconds; this is for testing purposes
    def selective_print(self, arr):
        arr_str = []
        index = 0
        while index < len(arr):
            arr_str.append(arr[index])
            index = index + int(0.25 / self.step_size)
        print(arr_str)

    # This graphs the membrane potential vs time of all of the neurons to output
    def graph(self):
        # Initializes the graph
        figure = plt.figure(figsize=(18, 18))
        timeticks = np.arange(0, 8.5, 1)
        grid = gridspec.GridSpec(self.neurons_to_output.__len__(), 1)
        index = 0

        # Adds a new plot for each neuron
        for neuron in self.neurons_to_output:
            graph = figure.add_subplot(grid[index, 0])
            potentialticks = np.arange(-90, 40, 10)
            neuron_data = neuron.get_output()
            row_count = neuron_data.__len__()
            graph.plot(self.time_arr[0:row_count], neuron_data[0:row_count])
            graph.set_title('Membrane Potential of %s' % neuron.get_name())
            graph.set_xlabel('Time (ms)')
            graph.set_ylabel('Membrane Potential (mV)')
            graph.axis([0, 8.5, -90, 40])
            graph.set_xticks(timeticks)
            graph.set_yticks(potentialticks)
            graph.grid(True)
            index += 1

        # Displays the graph
        plt.show()

# Creates the network.
network = AplysiaNet()

# This code gets the input from the user and translates into an input array for the network.
inputs = network.input
chem_input = [0]*((int)((1 / network.step_size)*(network.duration)) + 1)
mech_input = [0]*((int)((1 / network.step_size)*(network.duration)) + 1)
neuron2_input = [0]*((int)((1 / network.step_size)*(network.duration)) + 1)
network.handle_inputs(inputs[0], inputs[1], chem_input, 'chem')
network.handle_inputs(inputs[2], inputs[3], mech_input, 'mech')

# This code builds the circuit. For now, it is a test circuit with two typical IK neurons and a single excitatory* synapse.
# * the synapse hyperpolarizes too much. It should be excitatory with these params, but is mildly inhibitory instead.
neuron1 = Neuron(0.006, 0.25, -65, 8, -70, chem_input, 0.000008, 'Neuron1')
neuron2 = Neuron(0.006, 0.25, -65, 8, -70, neuron2_input, 0.000008, 'Neuron2')
synapse = Synapse(neuron1, neuron2, 30, 75, 20, 0.000008)
neurons = [neuron1, neuron2]
synapses = [synapse]

# The neurons and synapses are given to the network, and the simulation runs.
network.set_neurons(neurons)
network.set_synapses(synapses)
network.set_neurons_to_output(neurons)
network.run()

#TODO
#sanity checks 3-6
#more downsampling