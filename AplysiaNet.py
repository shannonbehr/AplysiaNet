from Interface import Interface
from Neuron import Neuron
from Synapse import Synapse, GSynapse
from tkinter import *
import csv
import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

class AplysiaNet:

    def __init__(self, duration, step_size):
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

        # The model is set up to run for duration seconds
        self.duration = duration

        # The frequency will be evaluated every step_size seconds
        self.step_size = step_size

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

    def set_synapses_to_output(self, synapses_to_output):
        self.synapses_to_output = synapses_to_output

    def run(self):
        # Creates a .csv file for the data
        data_file = open('AplysiaData.csv', 'w')
        writer = csv.writer(data_file, lineterminator= '\n')

        # Creates a .csv file for the synapse data
        syn_file = open('SynapseData.csv', 'w')
        syn_writer = csv.writer(syn_file, lineterminator='\n')

        # At each time step, update each neuron and run the output through the synapses to become the next inputs
        for index in range(0, (int)((1 / self.step_size)*(self.duration))):
            g_values = [self.t]
            write_g = 0

            for neuron in self.neurons:
                neuron.update(self.t)

            for synapse in synapses:
                synapse.update(self.t)

            for synapse in self.synapses_to_output:
                g_values.append(synapse.get_g())
                if synapse.write_g():
                    write_g = 1

            if write_g:
                syn_writer.writerow(g_values)

            self.t += self.step_size

        # This is for testing purposes; print the output of each neuron
        for neuron in self.neurons_to_output:
            self.selective_print(neuron.get_output())
            self.outputs.append(neuron.get_output())

        # This handles the output data to be written
        int_arr = list(range((int)(self.duration/self.step_size)))
        self.time_arr = [i * self.step_size for i in int_arr]

        output_arr = [self.time_arr] + self.outputs
        output_arr = zip(*output_arr)

        # This writes every 10th time step to a file if uncommented.
        #for i, val in enumerate(output_arr):
            #if i % 10 == 0:
                #writer.writerow(val)

        # Computes and prints the total run time of the simulation minus graphing
        end_time = time.time()
        total_time = end_time - self.start_time
        print('Total time = %s seconds' % total_time)

        # Closes the data files
        data_file.close()
        syn_file.close()

        # Creates the graph and displays it
        self.graph()

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
            if index*self.step_size <= start or index*self.step_size > end:
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
        start_time = 0
        end_time = 8.5 # Normally 8.5. For IK replication, 0.23636
        resolution = 1 # Normally 1. For IK replication, 0.01

        # Initializes the graph
        figure = plt.figure(figsize=(18, 18))
        timeticks = np.arange(start_time, end_time, resolution)
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
            graph.set_xlabel('Time (s)')
            graph.set_ylabel('Membrane Potential (mV)')
            graph.axis([start_time, end_time, -90, 40])
            graph.set_xticks(timeticks)
            graph.set_yticks(potentialticks)
            graph.grid(True)
            index += 1

        # Displays the graph
        plt.show()

step_size = 0.00001 #0.000008

# Creates the network.
network = AplysiaNet(8.5, step_size)

# This code gets the input from the user and translates into an input array for the network.
inputs = network.input
chem_input = [0]*((int)((1 / network.step_size)*(network.duration)) + 1)
mech_input = [0]*((int)((1 / network.step_size)*(network.duration)) + 1)
neuron2_input = [0]*((int)((1 / network.step_size)*(network.duration)) + 1)
network.handle_inputs(inputs[0], inputs[1], chem_input, 'chem')
network.handle_inputs(inputs[2], inputs[3], mech_input, 'mech')

# This code builds the circuit.
hco1 = Neuron(0.0005, 0.3, -65, 0.1, -70, chem_input, step_size, 'PC')
hco2 = Neuron(0.0005, 0.3, -65, 0.1, -58, neuron2_input, step_size, 'RC')
synapse1 = Synapse(hco1, hco2, 1.5, -80, 10, 20, 20, step_size)
synapse2 = Synapse(hco2, hco1, 1.5, -80, 10, 20, 20, step_size)
synapse3 = GSynapse(hco1, 1.5, 40, 10, 20, 20, step_size)
synapse4 = GSynapse(hco2, 1.5, 40, 10, 20, 20, step_size)
neurons = [hco1, hco2]
synapses = [synapse1, synapse2, synapse3, synapse4]
gsynapses = [synapse3, synapse4, synapse4, synapse4]

# The neurons and synapses are given to the network, and the simulation runs.
network.set_neurons(neurons)
network.set_synapses(synapses)
network.set_neurons_to_output(neurons)
network.set_synapses_to_output(gsynapses)
network.run()