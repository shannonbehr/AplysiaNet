class Synapse:

    def __init__(self, first_neuron, second_neuron, g_syn, e_syn, threshold, step_size):
        self.first_neuron = first_neuron
        self.second_neuron = second_neuron
        self.step_size = step_size

        # Time always starts at 0
        self.time = 0

        # 0 if synapse is off; weight of inputs if synapse is on; always starts at 0
        self.s = 0

        # Conductance
        self.g_syn = g_syn

        # Reversal potential (determines excitation/inhibition
        self.e_syn = e_syn

        # Threshold for synapse activation
        self.threshold = threshold

        # The index into the input and output arrays
        self.index = 0

    # Sets the membrane voltage to the given value; needed to compute Isyn
    def set_membrane_voltage(self):
        neuron_output = self.first_neuron.get_output()
        self.v_m = neuron_output[self.index]

    # Sets the s parameter to off (0) when presynaptic membrane potential is < the threshold or on (1) otherwise
    def set_s(self):
        if self.first_neuron.get_output()[self.index] < self.threshold:
            self.s = 0
        else:
            self.s = 1

    # Computes the output of the synapse
    def i_syn(self):
        return self.g_syn * self.s * (self.v_m - self.e_syn)

    # At each time step, computes the output of the synapse
    def update(self, time):
        self.time = time
        self.set_s()
        self.set_membrane_voltage()
        neuron_input = self.second_neuron.get_input()
        neuron_input[self.index] += self.i_syn()
        self.second_neuron.set_input(neuron_input)
        self.index += 1
