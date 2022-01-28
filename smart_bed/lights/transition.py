'''
Transitions a dmx lighting scene
'''

import threading


# set ammount each state will change by
def _get_transition_increments(differences, max_change):
    increments = [None for _ in differences]

    for i, values in enumerate(differences):
        increments[i] = [val / max_change for val in values]

    return increments


class Transition:
    def __init__(self, driver):
        self.driver = driver

        self.transition_end_states = []
        self.transition_duration = 0

        self.event = threading.Event()

        threading.Thread(target=self._run).start()


    # find maximum change needed to transition
    def _get_max_change(self, differences, end_states):
        current_state = self.driver.current()

        max_change = 1

        for i, obj in enumerate(end_states):
            values = obj['values']
            start = obj['start']
            end = obj['end']

            differences[i] = [0 for _ in values]

            for j, val in enumerate(values):
                current_value = current_state[start:end][j]
                difference = val - current_value

                differences[i][j] = difference

                if abs(difference) > max_change:
                    max_change = abs(difference)

        return max_change


    # get the step timeout duration
    def _get_transition_step(self, max_change):
        return self.transition_duration / max_change


    # creates the next states object
    def _next_states(self, end_states):
        current_state = self.driver.current()
        next_states = [None for _ in end_states]

        for i, obj in enumerate(end_states):
            start = obj['start']
            end = obj['end']

            next_states[i] = {
                'values': current_state[start:end][:],
                'start': start,
                'end': end
            }

        return next_states[:]


    def _run(self):
        self.event = threading.Event()

        end_states = None
        duration = None

        # transitioning loop
        while True:
            if self.transition_end_states != end_states or self.transition_duration != duration:
                end_states = self.transition_end_states
                duration = self.transition_duration

                differences = [None for _ in end_states]
                max_change = self._get_max_change(differences, end_states)
                step = self._get_transition_step(max_change)
                increments = _get_transition_increments(differences, max_change)
                next_states = self._next_states(end_states)

                count = 0

            if count < max_change:
                for i, obj in enumerate(next_states):
                    for j, val in enumerate(obj['values']):
                        next_states[i]['values'][j] = val + increments[i][j]

                self.driver.set(self.driver.inject(next_states))

                count += 1

                self.event.wait(step)


    def start(self, end_states, duration):
        self.event.clear()

        self.transition_end_states = end_states
        self.transition_duration = duration
