from Interface import Interface
from tkinter import *

class AplysiaNet:

    def __init__(self):
        root = Tk()
        interface = Interface(root)
        root.mainloop()

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

    # Later, get inputs from interface

    def run(self):
        for index in range(0, int(self.time + 1)):
            for neuron in self.neurons:
                neuron.update(self.time, neuron.get_next_current(self.time))
        for neuron in self.neurons:
            return neuron.get_output()

    # Generates an array of chemical or mechanical input to a neuron given stimulus start and end times
    def handleInputs(self, start, end, storage):
        for index in range(0, (int)(self.time + 1)):
            if index < start or index > end:
                storage[index] = 0
            else:
                storage[index] = self.current


network = AplysiaNet()