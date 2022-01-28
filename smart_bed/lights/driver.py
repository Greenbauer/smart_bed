'''
Defines the behavior of the dmx led light matrix
'''

import array
import threading
from ola.ClientWrapper import ClientWrapper


class LightsDriver:
    def __init__(self):
        self.current_state = [0 for _ in range(30)]
        self.new_state = [0 for _ in range(30)]

        threading.Thread(target=self._update).start()

        self._send()


    # send states to dmx
    def _send(self):
        def dmx_sent(dmx_state):
            if dmx_state:
                wrapper.Stop()

        # send dmx array
        universe = 1
        data = array.array('B', self.current())
        wrapper = ClientWrapper()
        client = wrapper.Client()
        client.SendDmx(universe, data, dmx_sent)
        wrapper.Run()


    # constanly check for new states and update the changes
    def _update(self):
        while True:
            new_state = [int(val) for val in self.new_state]

            if new_state != self.current_state:
                self.current_state = new_state[:]
                self._send()


    # set the new state to be updated
    def set(self, new_state):
        self.new_state = new_state


    # current updated state
    def current(self):
        return self.current_state[:]


    # inject a scene into the current state and return a new state
    def inject(self, inject_states):
        state = self.current()

        for obj in inject_states:
            start = obj['start']
            end = obj['end']

            state[start:end] = obj['values']

        return state
