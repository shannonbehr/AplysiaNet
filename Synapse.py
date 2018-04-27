class Synapse:

    def __init__(self, first_neuron, second_neuron, g_syn, e_syn, threshold, t_1, t_2, step_size):
        self.first_neuron = first_neuron
        self.second_neuron = second_neuron
        self.t_1 = t_1
        self.t_2 = t_2
        self.step_size = step_size

        # Time always starts at 0
        self.time = 0

        # 0 if synapse is off; weight of inputs if synapse is on; always starts at 0
        self.s = 0

        # Used for computing the "memory" of the synapse; functions like the old s
        self.g = 0

        # Peak value of g for this synapse over the course of the current simulation
        self.g_peak = 1

        # An intermediate parameter used to calculate g
        self.z = 0

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
        neuron_output = self.second_neuron.get_output()
        self.v_m = neuron_output[self.index]

    def write_g(self):
        return self.is_g_diff

    def get_g(self):
        return self.g

    # Sets the g parameter to some value between 0 and 1 to control "how on" the synapse is
    def set_g(self):
        old_g = self.g
        if self.first_neuron.get_output()[self.index] < self.threshold:
            x_t = 0
        else:
            x_t = 1
        self.g = self.eulers_method(self.g, (-(1 / self.t_2) * self.g + self.z)*1000)
        self.z = self.eulers_method(self.z, (-(1 / self.t_1) * self.z + x_t)*1000)
        if self.g == old_g:
            self.is_g_diff = 0
        else:
            self.is_g_diff = 1

    # Computes the output of the synapse
    def i_syn(self):
        return self.g_syn * (self.g/self.g_peak) * (self.e_syn - self.v_m)

    # This method computes the new voltage at each step. The following code was adapted from Tate Keller:
    def eulers_method(self, prev_value, value_step):
        return prev_value + self.step_size * value_step

    # At each time step, computes the output of the synapse
    def update(self, time):
        self.is_g_diff = 0
        self.time = time
        self.set_g()
        self.set_membrane_voltage()
        neuron_input = self.second_neuron.get_input()
        neuron_input[self.index] += self.i_syn()
        self.second_neuron.set_input(neuron_input)
        self.index += 1


class SimpleSynapse:

    def __init__(self, first_neuron, second_neuron, g_syn, e_syn, threshold, step_size, writer):
        self.first_neuron = first_neuron
        self.second_neuron = second_neuron
        self.step_size = step_size
        self.writer = writer

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
        neuron_output = self.second_neuron.get_output()
        self.v_m = neuron_output[self.index]

    # Sets the s parameter to off (0) when presynaptic membrane potential is < the threshold or on (1) otherwise
    def set_s(self):
        if self.first_neuron.get_output()[self.index] < self.threshold:
            self.s = 0
        else:
            self.s = 1

    # Computes the output of the synapse
    def i_syn(self):
        return self.g_syn * self.s * (self.e_syn - self.v_m)

    # At each time step, computes the output of the synapse
    def update(self, time):
        self.time = time
        self.set_s()
        self.set_membrane_voltage()
        neuron_input = self.second_neuron.get_input()
        neuron_input[self.index] += self.i_syn()
        self.second_neuron.set_input(neuron_input)
        self.index += 1

class GSynapse:

    def __init__(self, first_neuron, g_syn, e_syn, threshold, t_1, t_2, step_size):
        self.first_neuron = first_neuron
        self.t_1 = t_1
        self.t_2 = t_2
        self.step_size = step_size

        # Time always starts at 0
        self.time = 0

        # 0 if synapse is off; weight of inputs if synapse is on; always starts at 0
        self.s = 0

        # Used for computing the "memory" of the synapse; functions like the old s
        self.g = 0

        # Peak value of g for this synapse over the course of the current simulation
        self.g_peak = 1

        # An intermediate parameter used to calculate g
        self.z = 0

        # Conductance
        self.g_syn = g_syn

        # Reversal potential (determines excitation/inhibition
        self.e_syn = e_syn

        # Threshold for synapse activation
        self.threshold = threshold

        # The index into the input and output arrays
        self.index = 0

    def write_g(self):
        return self.is_g_diff

    def get_g(self):
        return self.g

    # Sets the g parameter to some value between 0 and 1 to control "how on" the synapse is
    def set_g(self):
        old_g = self.g
        if self.first_neuron.get_output()[self.index] < self.threshold:
            x_t = 0
        else:
            x_t = 1
        self.g = self.eulers_method(self.g, (-(1 / self.t_2) * self.g + self.z)*1000)
        self.z = self.eulers_method(self.z, (-(1 / self.t_1) * self.z + x_t)*1000)
        if self.g == old_g:
            self.is_g_diff = 0
        else:
            self.is_g_diff = 1

    # This method computes the new voltage at each step. The following code was adapted from Tate Keller:
    def eulers_method(self, prev_value, value_step):
        return prev_value + self.step_size * value_step

    # At each time step, computes the output of the synapse
    def update(self, time):
        self.is_g_diff = 0
        self.time = time
        self.set_g()
        self.index += 1