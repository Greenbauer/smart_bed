import time
import pytest
from test.util import light_state_checker
from smart_bed.lights.driver import LightsDriver
from smart_bed.lights.transition import Transition
from smart_bed.lights.state import State


DRIVER = LightsDriver()
INITIAL_STATE = DRIVER.current()
TRANSITION = Transition(DRIVER)
STATE = State()


@pytest.mark.run(after='test_lights_driver_inject')
def test_lights_transition():
    duration = 4

    DRIVER.set(INITIAL_STATE)

    # transition on
    end_state = DRIVER.inject([STATE.bottom_left(), STATE.middle()])

    TRANSITION.start([STATE.bottom_left(), STATE.middle()], duration)

    time.sleep(duration + 4)

    light_state_checker(DRIVER.current(), end_state)

    # transition off
    end_state = DRIVER.inject([STATE.bottom_left('off'), STATE.middle('off')])

    TRANSITION.start([STATE.bottom_left('off'), STATE.middle('off')], duration)

    time.sleep(duration + 4)

    light_state_checker(DRIVER.current(), end_state)
