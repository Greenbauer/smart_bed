'''
Controller for the bed lights
'''

from .transition import Transition
from .driver import LightsDriver
from .state import State


STATE = State()
DRIVER = LightsDriver()
TRANSITION = Transition(DRIVER)


# lower or raise the brighness of a scene
def set_brightness(state, amount=100):
    values = state['values'][:]

    for i, val in enumerate(values):
        if val > 0:
            values[i] = int(val * amount / 100)

            if values[i] > 254:
                values[i] = 255

        else:
            values[i] = 0

    state['values'] = values[:]

    return state


def current_scene():
    return DRIVER.current()


def _select_states(command):
    states = None
    command = command.lower()

    if command == 'scene on':
        states = [
            STATE.bottom_left(),
            STATE.bottom_right(),
            STATE.middle()
        ]

    elif command == 'guide light left':
        states = [
            set_brightness(STATE.bottom_left(), 50),
            STATE.bottom_right('off'),
            STATE.middle('off')
        ]

    elif command == 'guide light right':
        states = [
            STATE.bottom_left('off'),
            set_brightness(STATE.bottom_right(), 50),
            STATE.middle('off')
        ]

    elif command == 'guide lights':
        states = [
            set_brightness(STATE.bottom_left(), 50),
            set_brightness(STATE.bottom_right(), 50),
            STATE.middle('off')
        ]

    elif command == 'bottom left off':
        states = [
            STATE.bottom_left('off'),
        ]

    elif command == 'bottom right off':
        states = [
            STATE.bottom_right('off'),
        ]

    elif command == 'scene off':
        states = [
            STATE.bottom_left('off'),
            STATE.bottom_right('off'),
            STATE.middle('off')
        ]

    elif command == 'left lamp on':
        states = [
            STATE.top_left()
        ]

    elif command == 'left lamp off':
        states = [
            STATE.top_left('off')
        ]

    elif command == 'right lamp on':
        states = [
            STATE.top_right()
        ]

    elif command == 'right lamp off':
        states = [
            STATE.top_right('off')
        ]

    elif command == 'fun on':
        states = [
            STATE.bottom_left_fun(),
            STATE.bottom_right_fun(),
            STATE.middle_fun(),
            STATE.top_left(),
            STATE.top_right()
        ]

    elif command == 'all off':
        states = [
            STATE.bottom_left('off'),
            STATE.bottom_right('off'),
            STATE.middle('off'),
            STATE.top_left('off'),
            STATE.top_right('off')
        ]

    return states


def update_scene_context():
    STATE.update_context()


def set_scene(command, brightness=100):
    states = _select_states(command)
    states = [set_brightness(state, brightness) for state in states]

    DRIVER.set(DRIVER.inject(states))


def transition_scene(command, duration=1, brightness=100):
    states = _select_states(command)
    states = [set_brightness(state, brightness) for state in states]

    TRANSITION.start(states, duration)
