class Neuron:

    # This method initializes the neuron by setting the four IK parameters (a, b, c, and d) and the step size.
    def __init__(self, a, b, c, d, input, step_size, period_length, time):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.input = input
        self.step_size = step_size
        self.period_length = period_length
        self.time = time

        # The potential (v)  and recovery (u) parameters are initialized as described in the IK model.
        self.v = -70
        self.u = -70 * b

        # An array is initialized to hold the 43 frequency calculations, one for each 0.2 second interval.
        self.frequency = []

        # This will hold the outputs from synapses for use in finding the next current
        self.output = []
        for i in range(0, 34):
            self.output.append(0)

        # Since the biokinetic model always runs for 8.5 seconds, duration has been set to 8.5.
        self.duration = 8.5

    # Returns the output as an array of currents at each time step
    def get_output(self):
        return self.output

    # Returns the input array
    def get_input(self):
        return self.input

    # Sets the input array to the given input array
    def set_input(self, input):
        self.input = input

    # Sets the time to the given value and the current at this time to the given current
    def update(self, time, i):
        self.time = time
        self.input[(int)(time/self.period_length)] = i
        #stimulate the neuron here
        #return the current

    # This method updates the u and v parameter values using euler's method.
    def run_eulers_method(self):
        self.membrane_potential_dt()
        self.membrane_recovery_dt()
        return

    # This method computes the new voltage at each step. The following code was adapted from Tate Keller:
    def eulers_method(self, prev_voltage, voltage_step):
        return prev_voltage + self.step_size * voltage_step

    # This method sets the membrane potential after euler's method. The following code was adapted from Tate Keller:
    def membrane_potential_dt(self):
        # If v is above the threshold, v is assigned the reset parameter c.
        if self.v >= 30:
            self.v = self.c

        # If v is not above the threshold, euler's method is performed, and the step being passed in is multiplied by
        # 1000 to convert from ms to s.
        else:
            self.v = self.eulers_method(self.v, (((0.04 * self.v^2) + (5 * self.v) + 140 - self.u + self.input[self.time]) * 1000))
        return

    # This method sets the membrane recovery after euler's method. The following code was adapted from Tate Keller:
    def membrane_recovery_dt(self):
        # If u is above the threshold, u is assigned u plus the recovery parameter d.
        if self.u >= 30:
            self.u = self.u + self.d

        # If v is not above the threshold, euler's method is performed, and the step being passed in is multiplied by
        # 1000 to convert from ms to s.
        else:
            self.u = self.eulers_method(self.u, ((self.a * ((self.b * self.v) - self.u)) * 1000))
        return

    # This method takes in the start and end time of a period and calculates the average frequency by counting spikes.
    # A spike is defined as any point where the current, i, meets or exceeds 30.
    # This method is a different, hopefully improved version of Tate Keller's implementation.
    def calculate_frequency(self, start_time, end_time):
        current_time = start_time
        first_spike = -1
        last_spike = -1
        spike_count = 0

        # If we are still in the current period, count the spikes
        if end_time > current_time:
            if (spike_count == 0) and (self.input[current_time] >= 30):
                first_spike = current_time
                last_spike = current_time
                spike_count += 1
            elif (spike_count > 0) and (self.input[current_time] >= 30):
                last_spike = current_time
                spike_count +=1

        # No spikes
        if first_spike == -1 or last_spike == -1 or spike_count == 0:
            return 0

        # One spike
        if first_spike == last_spike:
            return 0

        # End of period successfully reached
        if (current_time == end_time or current_time + self.step_size >= end_time) and first_spike != -1 \
                and last_spike != -1 and spike_count > 0:
            period_time = last_spike - first_spike
            period_freq = period_time/spike_count
            return 1/period_freq

        # Error
        return -1

    # This method returns the start and end times of the current period. It is loosely based off of Tate's code.
    def get_start_and_end(self):
        total_periods = int(self.duration / self.period_length + 1)
        this_period = int(self.time / self.period_length)

        # If the current time falls within this period, return the start time and the end time
        for index in range (0, total_periods + 1):
            if this_period == index:
                return self.duration * index, self.duration * index + 1

        # Error
        return -1

    # This method returns the input current at the next time step.
    def get_next_current(self, time):
        if (int)(time/self.period_length) + 1 < (int)((1 / self.period_length)*(self.duration)):
            return self.input[(int)(time/self.period_length) + 1] + self.output[(int)(time/self.period_length)]
        else:
            return self.output[(int)(time/self.period_length)]
