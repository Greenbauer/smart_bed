import time
from datetime import datetime, timedelta
from test.util import light_state_checker, restore_status
from smart_bed.controller import rocker_fun_update, rocker_lamp_update, scene_update
from smart_bed.lights import current_scene, update_scene_context
from smart_bed.status import save, get


BLANK_SCENE = [0 for _ in range(30)]

TIME_SOON = (datetime.now() - timedelta(minutes=5)).isoformat()
TIME_LATE = (datetime.now() - timedelta(hours=2)).isoformat()


def test_controller_scene_update():
    # set an initial state
    save({'is_fun_mode': False, 'context': 'night'})

    update_scene_context()

    save({
        'is_occupied_left': True,
        'is_occupied_right': False,
        'time_last_occupied_left': None,
        'time_last_occupied_right': TIME_LATE
    })

    scene_update()
    time.sleep(10)

    # set as someone recently left bed during sleep
    save({'is_occupied_left': False, 'time_last_occupied_left': TIME_SOON})

    scene_update()
    time.sleep(20)

    # left guide light should be on
    expected_scene = BLANK_SCENE[:]
    expected_scene[0:2] = [16, 7]

    light_state_checker(current_scene(), expected_scene)

    # set as someone got in bed during day
    expected_scene = BLANK_SCENE[:]

    save({'context': 'mid day'})

    update_scene_context()

    save({'time_last_occupied_left': None, 'is_occupied_left': True})

    scene_update()
    time.sleep(20)

    # lights should be off
    light_state_checker(current_scene(), expected_scene)

    restore_status()


def test_controller_rocker_lamp_update():
    save({'context': 'mid day'})

    update_scene_context()

    expected_scene = current_scene()
    expected_scene[21:23] = [255, 255]

    # turn on a lamp
    rocker_lamp_update('click end', 'up', 'left')
    time.sleep(20)

    # lamp should be on
    light_state_checker(current_scene(), expected_scene)

    status = get()

    assert status['time_lamp_on_left'] is not None

    # turn off lamp
    expected_scene = BLANK_SCENE[:]

    rocker_lamp_update('click end', 'down', 'left')
    time.sleep(20)

    # lamp should be off
    light_state_checker(current_scene(), expected_scene)

    status = get()

    assert status['time_lamp_on_left'] is None

    restore_status()


def test_controller_rocker_fun_update():
    # exit fun mode with a lamp that was on
    save({
        'time_lamp_on_left': TIME_SOON,
        'is_fun_mode': True,
        'volume_change': 10
    })

    rocker_fun_update('hold', 'down')
    time.sleep(15)

    status = get()

    assert status['is_fun_mode'] is False
    assert status['time_lamp_on_left'] is not None
    assert status['volume_change'] == 0

    restore_status()
