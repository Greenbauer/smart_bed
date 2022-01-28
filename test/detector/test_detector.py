import os
import RPi.GPIO as GPIO
from smart_bed.detector import Detector


DETECTOR_LEFT = Detector(
    int(os.getenv('LOAD_CELL_LEFT_DT')),
    int(os.getenv('LOAD_CELL_LEFT_SCK')),
    'left',
    [80, 40]
)

DETECTOR_RIGHT = Detector(
    int(os.getenv('LOAD_CELL_RIGHT_DT')),
    int(os.getenv('LOAD_CELL_RIGHT_SCK')),
    'right',
    [80, 40]
)


def _clean():
    GPIO.cleanup()


def test_detectors():
    try:

        DETECTOR_LEFT.measure()
        DETECTOR_RIGHT.measure()

        weight_left = abs(DETECTOR_LEFT.weight)
        weight_right = abs(DETECTOR_RIGHT.weight)

        # make sure load cells are connected and functioning
        assert weight_left > 0.0
        assert weight_right > 0.0

        _clean()

    except (KeyboardInterrupt, SystemExit):
        _clean()
