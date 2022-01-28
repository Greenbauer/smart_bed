'''
Defines led color values for different parts of the dmx lighing matrix

   r,  g,  b, ww, cw
[  0,  1,  2,  3,  4 ] bottom left led strip
[  6,  7,  8,  9, 10 ] bottom right led strip
[ 12, 13, 14, 15, 16 ] top middle led strip
[ 18, 19, 20, 21, 22 ] left side led strip
[ 24, 25, 26, 27, 28 ] right side led strip
'''

from smart_bed.status import get


class State():
    def __init__(self):
        self.update_context()

    def update_context(self):
        status = get()

        self.context = status['context'].lower()

    def bottom_left(self, state=''):
        if state == 'off':
            return {
                'values': [0, 0, 0, 0, 0],
                'start': 0,
                'end': 5
            }

        context = self.context

        if context == 'morning':
            return {
                'values': [0, 0, 0, 18, 37],
                'start': 0,
                'end': 5
            }

        if context == 'mid day':
            return {
                'values': [0, 0, 0, 35, 25],
                'start': 0,
                'end': 5
            }

        return {
            'values': [35, 15, 0, 0, 0],
            'start': 0,
            'end': 5
        }

    def bottom_left_fun(self):
        context = self.context

        if context == 'night':
            return {
                'values': [90, 5, 10, 0, 0],
                'start': 0,
                'end': 5
            }

        return {
            'values': [0, 0, 0, 70, 50],
            'start': 0,
            'end': 5
        }

    def bottom_right(self, state=''):
        if state == 'off':
            return {
                'values': [0, 0, 0, 0, 0],
                'start': 6,
                'end': 11
            }

        context = self.context

        if context == 'morning':
            return {
                'values': [0, 0, 0, 18, 37],
                'start': 6,
                'end': 11
            }

        if context == 'mid day':
            return {
                'values': [0, 0, 0, 35, 25],
                'start': 6,
                'end': 11
            }

        return {
            'values': [35, 15, 0, 0, 0],
            'start': 6,
            'end': 11
        }

    def bottom_right_fun(self):
        context = self.context

        if context == 'night':
            return {
                'values': [90, 5, 10, 0, 0],
                'start': 6,
                'end': 11
            }

        return {
            'values': [0, 0, 0, 70, 50],
            'start': 6,
            'end': 11
        }

    def middle(self, state=''):
        if state == 'off':
            return {
                'values': [0, 0, 0, 0, 0],
                'start': 12,
                'end': 17
            }

        context = self.context

        if context == 'morning':
            return {
                'values': [0, 0, 0, 32, 42],
                'start': 12,
                'end': 17
            }

        if context == 'mid day':
            return {
                'values': [0, 0, 0, 37, 37],
                'start': 12,
                'end': 17
            }

        return {
            'values': [35, 10, 12, 0, 0],
            'start': 12,
            'end': 17
        }

    def middle_fun(self):
        context = self.context

        if context == 'night':
            return {
                'values': [255, 0, 30, 80, 0],
                'start': 12,
                'end': 17
            }

        return {
            'values': [0, 0, 0, 85, 85],
            'start': 12,
            'end': 17
        }

    def top_left(self, state=''):
        if state == 'off':
            return {
                'values': [0, 0, 0, 0, 0],
                'start': 18,
                'end': 23
            }

        context = self.context

        if context == 'night':
            return {
                'values': [0, 0, 0, 255, 50],
                'start': 18,
                'end': 23
            }

        return {
            'values': [0, 0, 0, 255, 255],
            'start': 18,
            'end': 23
        }

    def top_right(self, state=''):
        if state == 'off':
            return {
                'values': [0, 0, 0, 0, 0],
                'start': 24,
                'end': 29
            }

        context = self.context

        if context == 'night':
            return {
                'values': [0, 0, 0, 255, 50],
                'start': 24,
                'end': 29
            }

        return {
            'values': [0, 0, 0, 255, 255],
            'start': 24,
            'end': 29
        }
