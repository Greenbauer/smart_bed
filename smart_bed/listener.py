'''
Listens to user input devices
'''

import os
import threading
import time
import sys
import RPi.GPIO as GPIO
from smart_bed.detector import Detector
from smart_bed.rocker import Rocker


DETECTOR_LEFT = Detector(
    int(os.getenv('LOAD_CELL_LEFT_DT')),
    int(os.getenv('LOAD_CELL_LEFT_SCK')),
    'left',
    [90, 40]
)
DETECTOR_RIGHT = Detector(
    int(os.getenv('LOAD_CELL_RIGHT_DT')),
    int(os.getenv('LOAD_CELL_RIGHT_SCK')),
    'right',
    [90, 45]
)

ROCKER_LEFT = Rocker(
    int(os.getenv('ROCKER_LEFT_UP')),
    int(os.getenv('ROCKER_LEFT_DOWN')),
    'left'
)
ROCKER_RIGHT = Rocker(
    int(os.getenv('ROCKER_RIGHT_UP')),
    int(os.getenv('ROCKER_RIGHT_DOWN')),
    'right'
)


def _loop(runner):
    while True:
        try:
            runner()

        except (KeyboardInterrupt, SystemExit):
            GPIO.cleanup()
            sys.exit()


def _detector_listener():
    def run():
        DETECTOR_LEFT.update_occupancy()
        DETECTOR_RIGHT.update_occupancy()

        time.sleep(3)

    _loop(run)


def _rocker_listener():
    def run():
        ROCKER_LEFT.update_click()
        ROCKER_RIGHT.update_click()

    _loop(run)


threading.Thread(target=_detector_listener).start()
threading.Thread(target=_rocker_listener).start()
