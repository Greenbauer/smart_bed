'''
Defines the behavior of the lamp rocker switches
'''

import time
import RPi.GPIO as GPIO


class RockerDriver:
    def __init__(self, pin):
        self.pin = pin
        self.state = None
        self.hold_time = 0
        self.click_time = 0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def _check_hold(self, next_state):
        current_state = self.state

        if current_state in ['click start', 'hold']:
            if self.hold_time + 1 < time.time():
                next_state = 'hold'

        else:
            self.hold_time = time.time()

        return next_state

    # attempt to supress any random noise that detects a click event
    def _check_click_end(self, next_state):
        if self.click_time + .9 < time.time():
            next_state = 'click end'

        else:
            self.click_time = time.time()

        return next_state

    def is_clicked(self):
        current_state = self.state
        next_state = None

        if GPIO.input(self.pin) is GPIO.HIGH:
            next_state = 'click start'
            next_state = self._check_hold(next_state)

        elif current_state in ['click start', 'hold']:
            next_state = self._check_click_end(next_state)

        if next_state is not current_state:
            self.state = next_state

        return next_state
