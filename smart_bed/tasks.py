'''
Performs routines that update the bed status
'''

import time
import threading
import schedule
from smart_bed.context import update_context
from smart_bed.controller import rocker_lamp_update, scene_update
from smart_bed.status import get
from smart_bed.util import is_time_expired


# turn off any lamps that have been on a while
def _turn_off_lamps(current_status):
    time_lamp_on_left = current_status['time_lamp_on_left']
    time_lamp_on_right = current_status['time_lamp_on_right']

    if is_time_expired(time_lamp_on_left, hours=1) is True:
        rocker_lamp_update('click end', 'down', 'left')

    if is_time_expired(time_lamp_on_right, hours=1) is True:
        rocker_lamp_update('click end', 'down', 'right')


# automatically set the bed scene
def _set_scene(current_status):
    context = current_status['context']

    if context == 'night':
        scene_update()


def _run_tasks():
    try:
        # to update the lighing color temperatures
        update_context()

        current_status = get()

        # things to check and change
        _turn_off_lamps(current_status)
        time.sleep(3)

        _set_scene(current_status)

    except Exception as e:
        print('ERROR: Running Task', e)
        _run_tasks()


def _schedule_loop():
    schedule.every(15).minutes.do(_run_tasks)

    while True:
        schedule.run_pending()
        time.sleep(1)


threading.Thread(target=_schedule_loop).start()
