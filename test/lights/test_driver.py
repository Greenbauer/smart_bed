import time
from smart_bed.lights.driver import LightsDriver

DRIVER = LightsDriver()
INITIAL_STATE = DRIVER.current()


def test_lights_driver_set():
    state = INITIAL_STATE[:]
    state[0] = 200

    DRIVER.set(state)
    time.sleep(2)

    assert DRIVER.current() == state


def test_lights_driver_inject():
    array = [
        {
            'values': [10, 1],
            'start': 6,
            'end': 8
        },
        {
            'values': [255, 0, 100],
            'start': 15,
            'end': 18
        }
    ]

    expected_state = DRIVER.current()
    expected_state[6] = 10
    expected_state[7] = 1
    expected_state[15] = 255
    expected_state[16] = 0
    expected_state[17] = 100

    new_state = DRIVER.inject(array)

    assert new_state == expected_state

    array2 = [
        {
            'values': [1, 33],
            'start': 0,
            'end': 2
        },
        {
            'values': [55, 0, 100],
            'start': 26,
            'end': 29
        }
    ]

    expected_state2 = DRIVER.current()
    expected_state2[0] = 1
    expected_state2[1] = 33
    expected_state2[26] = 55
    expected_state2[27] = 0
    expected_state2[28] = 100

    new_state2 = DRIVER.inject(array2)

    assert new_state2 == expected_state2
