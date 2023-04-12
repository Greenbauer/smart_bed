'''
Handles the functionality of when the bed is occupied
'''

from datetime import datetime
from smart_bed.status import get, save
from smart_bed.controller import scene_update
from .driver import HX711


class Detector:

    def __init__(self, dout, pd_sck, side, weight_thresholds):
        self.load_cell = HX711(dout, pd_sck)
        self.side = side
        self.opposite_side = 'left' if side.lower() == 'left' else 'right'
        self.min_weight_threshold = weight_thresholds[0]
        self.max_weight_threshold = weight_thresholds[1]
        self.weight = 0

        self.is_occupied = None
        self.time_last_occupied = None
        self.is_occupied_opposite = None
        self.is_fun_mode = None

        self._get_status()

        reference_unit = -10000

        self.load_cell.set_reading_format("MSB", "MSB")
        self.load_cell.set_reference_unit(reference_unit)

        self.load_cell.reset()

        print(side + ' detector is ready')

    def _get_status(self):
        status = get()

        self.is_occupied = status['is_occupied_' + self.side]
        self.time_last_occupied = status['time_last_occupied_' + self.side]
        self.is_occupied_opposite = status['is_occupied_' + self.opposite_side]
        self.is_fun_mode = status['is_fun_mode']

    def _tare(self, prev_weight, next_weight):
        # only tare on load and empty bed or if weight significantly changes
        if prev_weight == 0:
            self._get_status()

            if self.is_occupied is False:
                self.load_cell.tare()
                self.measure()

        elif (
            prev_weight > next_weight and
            abs(prev_weight - next_weight) > self.min_weight_threshold
        ):
            # self.load_cell.tare()
            self.measure()

    def measure(self):
        prev_weight = self.weight
        weight = self.load_cell.get_weight(7)

        self.load_cell.power_down()
        self.load_cell.power_up()

        if weight > self.max_weight_threshold * 1.3:
            weight = self.max_weight_threshold * 1.3

        self.weight = weight
        self._tare(prev_weight, weight)

    def update_occupancy(self):
        self.measure()

        if self.is_fun_mode is not True:
            weight = self.weight

            is_occupied = self.is_occupied

            min_weight_threshold = self.min_weight_threshold

            if self.is_occupied_opposite:
                min_weight_threshold *= self.max_weight_threshold / self.min_weight_threshold

            if weight > self.max_weight_threshold:
                is_occupied = True
            elif weight <= min_weight_threshold:
                is_occupied = False

            # print('DETECTOR: ' + self.side + ':', is_occupied, weight)

            if self.is_occupied is None or is_occupied is not self.is_occupied:
                if is_occupied is False:
                    self.time_last_occupied = datetime.now().isoformat()

                else:
                    self.time_last_occupied = None

                self.is_occupied = is_occupied

                save({
                    'time_last_occupied_' + self.side: self.time_last_occupied,
                    'is_occupied_' + self.side: is_occupied
                })

                scene_update()
