class Synapse:

    def __init__(self, first_neuron, second_neuron, s, g_syn, e_syn):
        self.first_neuron = first_neuron
        self.second_neuron = second_neuron

        # threshold
        self.s = s

        # 0 if synapse is off; weight of inputs if synapse is on
        self.g_syn = g_syn

        # reversal potential (determines excitation/inhibition
        self.e_syn = e_syn

    # Sets the membrane voltage to the given value; needed to compute Isyn
    def set_membrane_voltage(self, v_m):
        self.vm = v_m

    # Computes the output of the synapse
    def i_syn(self):
        return self.g_syn * self.s * (self.v_m + self.e_syn)