import time
from datetime import datetime, timedelta
from test.util import restore_status
from smart_bed.status import get, save
from smart_bed.tasks import _turn_off_lamps


TIME_SOON = (datetime.now() - timedelta(minutes=5)).isoformat()
TIME_LATE = (datetime.now() - timedelta(hours=2)).isoformat()


def test_task_turn_off_lamps():
    # make sure left lamp on was turned off
    save({'time_lamp_on_left': TIME_SOON, 'time_lamp_on_right': TIME_LATE})

    status = get()

    _turn_off_lamps(status)
    time.sleep(10)

    status = get()

    assert status['time_lamp_on_left'] is not None
    assert status['time_lamp_on_right'] is None

    restore_status()
