'''
Command various functionalities of the bed
'''

import time
from datetime import datetime
from smart_bed.status import get, save
from smart_bed.lights import transition_scene, set_scene
from smart_bed.api import post_status
from smart_bed.util import is_time_expired


def _was_recently_occupied(current_status, side, minutes=5):
    return current_status['time_last_occupied_' + side] is not None and not is_time_expired(
        current_status['time_last_occupied_' + side], minutes=minutes)


def scene_update():
    current_status = get()

    is_fun_mode = current_status['is_fun_mode']
    context = current_status['context'].lower()

    is_occupied_left = current_status['is_occupied_left']
    is_occupied_right = current_status['is_occupied_right']

    if is_fun_mode is not True:
        command = 'scene off'

        # no one is occupying the bed
        if (
            is_occupied_left is False and is_occupied_right is False and
            (
                _was_recently_occupied(current_status, 'left', 3) is True or
                _was_recently_occupied(current_status, 'right', 3) is True
            )
        ):
            command = 'scene on'

        if context == 'night':
            was_recently_occupied_left = _was_recently_occupied(
                current_status, 'left', 15)
            was_recently_occupied_right = _was_recently_occupied(
                current_status, 'right', 15)

            # both sides of bed were recently occupied
            if (
                was_recently_occupied_left is True and
                was_recently_occupied_right is True
            ):
                command = 'guide lights'

            # only left side of bed was recently occupied
            elif was_recently_occupied_left is True:
                command = 'guide light left'

            # only right side of bed was recently occupied
            elif was_recently_occupied_right is True:
                command = 'guide light right'

            # no one is occupying the bed
            elif is_occupied_left is False and is_occupied_right is False:
                command = 'scene on'

        # print('UPDATE SCENE TO:', command, 'l:',
        #  was_recently_occupied_left, 'r:', was_recently_occupied_right, current_status['time_last_occupied_left'])

        # set context scene
        if command == 'scene on':
            transition_scene(command)

            time.sleep(1)

            if context != 'night':
                transition_scene('scene off', 60 * 12)  # 12 minutes

        else:
            transition_scene(command)

        post_status()


scene_update()


def rocker_lamp_update(state, direction, side):
    command = None

    if state == 'click end':
        # turn off lamp
        if direction == 'down':
            command = side + ' lamp off'
            save({'time_lamp_on_' + side: None})

        # turn on lamp
        elif direction == 'up':
            command = side + ' lamp on'
            save({'time_lamp_on_' + side: datetime.now().isoformat()})

    # enter fun mode
    elif state == 'hold' and direction == 'up':
        command = 'fun on'
        save({'is_fun_mode': True, 'time_fun_mode_on': datetime.now().isoformat()})
        post_status()

    # print('UPDATE LAMP TO:', command, direction, state)

    if command == 'fun on':
        transition_scene(command, 5)
        time.sleep(5)

    elif command is not None:
        set_scene(command)


def lamps_update():
    status = get()

    is_lamp_on_left = status['time_lamp_on_left'] is not None
    is_lamp_on_right = status['time_lamp_on_right'] is not None

    time.sleep(2)

    if is_lamp_on_left is True:
        rocker_lamp_update('click end', 'up', 'left')
    else:
        rocker_lamp_update('click end', 'down', 'left')

    time.sleep(2)

    if is_lamp_on_right is True:
        rocker_lamp_update('click end', 'up', 'right')
    else:
        rocker_lamp_update('click end', 'down', 'right')


lamps_update()


def rocker_fun_update(state, direction, volume_change=0):
    command = None

    # change volume
    if state == 'click end':
        save({'volume_change': volume_change})
        post_status()

    # exit fun mode
    elif state == 'hold' and direction == 'down':
        command = 'all off'
        save({'is_fun_mode': False, 'time_fun_mode_on': None, 'volume_change': 0})
        post_status()

    # print('UPDATE FUN MODE TO:', command, direction, state, volume_change)

    if command == 'scene on':
        transition_scene(command, 5)

    elif command is not None:
        set_scene(command)
