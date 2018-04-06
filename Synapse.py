class Synapse:

    def __init__(self, first_neuron, second_neuron, s, g_syn, e_syn, step_size, time):
        self.first_neuron = first_neuron
        self.second_neuron = second_neuron
        self.step_size = step_size
        self.time = time

        # threshold
        self.s = s

        # 0 if synapse is off; weight of inputs if synapse is on
        self.g_syn = g_syn

        # reversal potential (determines excitation/inhibition
        self.e_syn = e_syn

    # Sets the membrane voltage to the given value; needed to compute Isyn
    def set_membrane_voltage(self):
        neuron_output = self.first_neuron.get_output()
        self.v_m = neuron_output[(int)(self.time/self.step_size)]

    # Sets the s parameter to off (0) when presynaptic membrane potential is < 20 mV or on (1) otherwise
    def set_s(self):
        if self.second_neuron.get_input()[(int)(self.time/self.step_size)] < 20:
            self.s = 0
        else:
            self.s = 1

    # Computes the output of the synapse
    def i_syn(self):
        return self.g_syn * self.s * (self.v_m - self.e_syn)

    # At each time step, computes the output of the synapse
    def update(self, time):
        self.time = time
        self.set_membrane_voltage()
        self.set_s()
        neuron_input = self.second_neuron.get_input()
        neuron_input[(int)(self.time/self.step_size)] += self.i_syn()
        self.second_neuron.set_input(neuron_input)
