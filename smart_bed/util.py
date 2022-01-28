'''
Various reusable functions
'''

from datetime import datetime, timedelta
from dateutil.parser import parse


# calculates if a timestamp is beyond a limit
def is_time_expired(timestamp, **duration):
    if timestamp is not None:
        timestamp = parse(timestamp).replace(tzinfo=None)

        if timestamp < datetime.now() - timedelta(**duration):
            return True

    return False
