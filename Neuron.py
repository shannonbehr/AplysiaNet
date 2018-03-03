class Neuron:

    # This method initializes the neuron by setting the four IK parameters (a, b, c, and d) and the step size.
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

        # The step size value is that used by Greg Sutton; the same value was chosen here to integrate the two models.
        self.step_size = 0.000008

        # The model is set up to run for 8.5 seconds
        self.duration = 8.5

        # The frequency will be evaluated every 0.25 seconds
        self.period_length = 0.25

        # The model starts at time = 0 seconds
        self.time = 0

        # The potential (v)  and recovery (u) parameters are initialized as described in the IK model.
        self.v = -70
        self.u = -70 * b

        # An array is initialized to hold the 43 frequency calculations, one for each 0.2 second interval.
        self.frequency = []

    # This administers a current, i, to the neuron
    # WRITE THIS METHOD!!
    def stimulate(self, i):
        self.i = i
        return

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
            self.v = self.eulers_method(self.v, (((0.04 * self.v^2) + (5 * self.v) + 140 - self.u + self.i) * 1000))
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
            if (spike_count == 0) and (self.i >= 30):
                first_spike = current_time
                last_spike = current_time
                spike_count += 1
            elif (spike_count > 0) and (self.i >= 30):
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

