'''
Finds and resolves information external to the bed
'''

from datetime import datetime, timedelta
import os
from astral.sun import sun
from astral import LocationInfo
import tzlocal
from smart_bed.lights import update_scene_context
from smart_bed.status import save


# save bed location in house
ROOM = os.getenv('DEVICE_ROOM')
save({'room': ROOM})

# sync with the location of the sun
TZ = tzlocal.get_localzone()
LATITUDE = float(os.getenv('DEVICE_LATITUDE'))
LONGITUDE = float(os.getenv('DEVICE_LONGITUDE'))

LOCATION = LocationInfo(latitude=LATITUDE, longitude=LONGITUDE)


def _time(context):
    position = sun(LOCATION.observer, tzinfo=TZ)

    return position[context].replace(tzinfo=None)


def update_context():
    now = datetime.now()

    context = 'morning'

    if (
        now < _time('sunrise') + timedelta(minutes=-30) or
        now > _time('sunset') + timedelta(hours=2)
    ):
        context = 'night'

    elif now > _time('sunrise') + timedelta(hours=4):
        context = 'mid day'

    save({'context': context})
    update_scene_context()
