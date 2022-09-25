'''
Handles the functionality of the lamp rocker switches
'''

import time
from smart_bed.status import get
from smart_bed.controller import rocker_lamp_update, rocker_fun_update
from .driver import RockerDriver


class Rocker:
    def __init__(self, pin_up, pin_down, side):
        self.rocker_up = RockerDriver(pin_up)
        self.rocker_down = RockerDriver(pin_down)
        self.side = side.lower()

        self.state = None

        self.volume_change = 0
        self._get_status()

    def _get_status(self):
        status = get()

        if status:
            self.is_fun_mode = status['is_fun_mode']
            self.volume_change = status['volume_change']

    def _handle_fun(self, state, direction):
        volume_change = self.volume_change

        # changing the volume
        if state == 'click end':
            if direction == 'up':
                volume_change += 20

            elif direction == 'down':
                volume_change -= 20

            if volume_change > 100:
                volume_change = 100
            elif volume_change < -100:
                volume_change = -100

        if self.state != 'hold':
            rocker_fun_update(state, direction, volume_change)

            self.volume_change = volume_change
            self._get_status()

    def _handle_lamp(self, state, direction):
        # dont use normal click end logic after a button hold down
        if state == 'end' and self.state == 'hold':
            state = None

        if self.state != 'hold':
            rocker_lamp_update(state, direction, self.side)

            self._get_status()

    def update_click(self):
        state_up = self.rocker_up.is_clicked()
        state_down = self.rocker_down.is_clicked()

        direction = None
        state = None

        if state_up is not None:
            state = state_up
            direction = 'up'

        elif state_down is not None:
            state = state_down
            direction = 'down'

        # only need to know what happens when a button is held down or released
        if state != 'click start' and state is not None:
            time.sleep(.2)
            if self.is_fun_mode is True:
                self._handle_fun(state, direction)

            else:
                self._handle_lamp(state, direction)

            self.state = state
