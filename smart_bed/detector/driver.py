'''
Defines the behavior of the load cells used to detect when the bed is occupied


Source: https://github.com/tatobari/hx711py
'''

import time
import threading
import RPi.GPIO as GPIO


class HX711:

    def __init__(self, dout, pd_sck, gain=128):
        self.pd_sck = pd_sck

        self.dout = dout

        # Mutex for reading from the HX711, in case multiple threads in client
        # software try to access get values from the class at the same time.
        self.read_lock = threading.Lock()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pd_sck, GPIO.OUT)
        GPIO.setup(self.dout, GPIO.IN)

        self.gain = 0

        # The value returned by the hx711 that corresponds to your reference
        # unit AFTER dividing by the SCALE.
        self.reference_unit = 1
        self.reference_unit_b = 1

        self.offset = 1
        self.offset_b = 1
        self.last_val = int(0)

        self.debug_printing = False

        self.byte_format = 'MSB'
        self.bit_format = 'MSB'

        self._set_gain(gain)

        # Think about whether this is necessary.
        time.sleep(1)

    def _is_ready(self):
        return GPIO.input(self.dout) == 0

    def _set_gain(self, gain):
        if gain == 128:
            self.gain = 1
        elif gain == 64:
            self.gain = 3
        elif gain == 32:
            self.gain = 2

        GPIO.output(self.pd_sck, False)

        # Read out a set of raw bytes and throw it away.
        self._read_raw_bytes()

    def _get_gain(self):
        if self.gain == 1:
            return 128
        if self.gain == 3:
            return 64
        if self.gain == 2:
            return 32

        # Shouldn't get here.
        return 0

    def _read_next_bit(self):
        # Clock HX711 Digital Serial Clock (pd_sck). dout will be
        # ready 1us after pd_sck rising edge, so we sample after
        # lowering PD_SCL, when we know dout will be stable.
        GPIO.output(self.pd_sck, True)
        GPIO.output(self.pd_sck, False)
        value = GPIO.input(self.dout)

        # Convert Boolean to int and return it.
        return int(value)

    def _read_next_byte(self):
        byte_value = 0

        # Read bits and build the byte from top, or bottom, depending
        # on whether we are in MSB or LSB bit mode.
        for _ in range(8):
            if self.bit_format == 'MSB':
                byte_value <<= 1
                byte_value |= self._read_next_bit()
            else:
                byte_value >>= 1
                byte_value |= self._read_next_bit() * 0x80

        # Return the packed byte.
        return byte_value

    def _read_raw_bytes(self):
        # Wait for and get the Read Lock, incase another thread is already
        # driving the HX711 serial interface.
        self.read_lock.acquire()

        # Wait until HX711 is ready for us to read a sample.
        while not self._is_ready():
            pass

        # Read three bytes of data from the HX711.
        first_byte = self._read_next_byte()
        second_byte = self._read_next_byte()
        third_byte = self._read_next_byte()

        # HX711 Channel and gain factor are set by number of bits read
        # after 24 data bits.
        for _ in range(self.gain):
            # Clock a bit out of the HX711 and throw it away.
            self._read_next_bit()

        # Release the Read Lock, now that we've finished driving the HX711
        # serial interface.
        self.read_lock.release()

        # Depending on how we're configured, return an orderd list of raw byte
        # values.
        if self.byte_format == 'LSB':
            return [third_byte, second_byte, first_byte]

        return [first_byte, second_byte, third_byte]

    def _read_long(self):
        # Get a sample from the HX711 in the form of raw bytes.
        data_bytes = self._read_raw_bytes()

        if self.debug_printing:
            print(data_bytes,)

        # Join the raw bytes into a single 24bit 2s complement value.
        twos_complement_value = (
            (data_bytes[0] << 16) | (data_bytes[1] << 8) | data_bytes[2]
        )

        if self.debug_printing:
            print("Twos: 0x%06x" % twos_complement_value)

        # Convert from 24bit twos-complement to a signed value.
        signed_in_value = -(twos_complement_value & 0x800000) + \
            (twos_complement_value & 0x7fffff)

        # Record the latest sample value we've read.
        self.last_val = signed_in_value

        # Return the sample value we've read from the HX711.
        return int(signed_in_value)

    def _read_average(self, times=3):
        # Make sure we've been asked to take a rational amount of samples.
        if times <= 0:
            raise ValueError("HX711()::_read_average(): times must >= 1!!")

        # If we're only average across one value, just read it and return it.
        if times == 1:
            return self._read_long()

        # If we're averaging across a low amount of values, just take the
        # median.
        if times < 5:
            return self._read_median(times)

        # If we're taking a lot of samples, we'll collect them in a list, remove
        # the outliers, then take the mean of the remaining set.
        value_list = []

        for _ in range(times):
            value_list += [self._read_long()]

        value_list.sort()

        # We'll be trimming 20% of outlier samples from top and bottom of collected set.
        trim_amount = int(len(value_list) * 0.2)

        # Trim the edge case values.
        value_list = value_list[trim_amount:-trim_amount]

        # Return the mean of remaining samples.
        return sum(value_list) / len(value_list)

    # A median-based read method, might help when getting random value spikes
    # for unknown or CPU-related reasons

    def _read_median(self, times=3):
        if times <= 0:
            raise ValueError(
                "HX711::_read_median(): times must be greater than zero!")

        # If times == 1, just return a single reading.
        if times == 1:
            return self._read_long()

        value_list = []

        for _ in range(times):
            value_list += [self._read_long()]

        value_list.sort()

        # If times is odd we can just take the centre value.
        if (times & 0x1) == 0x1:
            return value_list[len(value_list) // 2]

        # If times is even we have to take the arithmetic mean of
        # the two middle values.
        midpoint = len(value_list) / 2
        return sum(value_list[midpoint:midpoint+2]) / 2.0

    # Compatibility function, uses channel A version

    def get_value(self, times=3):
        return self.get_value_a(times)

    def get_value_a(self, times=3):
        return self._read_median(times) - self.get_offset_a()

    def get_value_b(self, times=3):
        # for channel B, we need to _set_gain(32)
        gain = self._get_gain()
        self._set_gain(32)
        value = self._read_median(times) - self.get_offset_b()
        self._set_gain(gain)
        return value

    # Compatibility function, uses channel A version
    def get_weight(self, times=3):
        return self.get_weight_a(times)

    def get_weight_a(self, times=3):
        value = self.get_value_a(times)
        value = value / self.reference_unit
        return value

    def get_weight_b(self, times=3):
        value = self.get_value_b(times)
        value = value / self.reference_unit_b
        return value

    # Sets tare for channel A for compatibility purposes

    def tare(self, times=15):
        return self.tare_a(times)

    def tare_a(self, times=15):
        # Backup reference_unit value
        backup_reference_unit = self.get_reference_unit_a()
        self.set_reference_unit_a(1)

        value = self._read_average(times)

        if self.debug_printing:
            print("Tare A value:", value)

        self.set_offset_a(value)

        # Restore the reference unit, now that we've got our offset.
        self.set_reference_unit_a(backup_reference_unit)

        return value

    def tare_b(self, times=15):
        # Backup reference_unit value
        backup_reference_unit = self.get_reference_unit_b()
        self.set_reference_unit_b(1)

        # for channel B, we need to _set_gain(32)
        backup_gain = self._get_gain()
        self._set_gain(32)

        value = self._read_average(times)

        if self.debug_printing:
            print("Tare B value:", value)

        self.set_offset_b(value)

        # Restore gain/channel/reference unit settings.
        self._set_gain(backup_gain)
        self.set_reference_unit_b(backup_reference_unit)

        return value

    def set_reading_format(self, byte_format="LSB", bit_format="MSB"):
        if byte_format == "LSB":
            self.byte_format = byte_format
        elif byte_format == "MSB":
            self.byte_format = byte_format
        else:
            raise ValueError("Unrecognised byte_format: \"%s\"" % byte_format)

        if bit_format == "LSB":
            self.bit_format = bit_format
        elif bit_format == "MSB":
            self.bit_format = bit_format
        else:
            raise ValueError("Unrecognised bitformat: \"%s\"" % bit_format)

    # sets offset for channel A for compatibility reasons

    def set_offset(self, offset):
        self.set_offset_a(offset)

    def set_offset_a(self, offset):
        self.offset = offset

    def set_offset_b(self, offset):
        self.offset_b = offset

    def get_offset(self):
        return self.get_offset_a()

    def get_offset_a(self):
        return self.offset

    def get_offset_b(self):
        return self.offset_b

    def set_reference_unit(self, reference_unit):
        self.set_reference_unit_a(reference_unit)

    def set_reference_unit_a(self, reference_unit):
        # Make sure we aren't asked to use an invalid reference unit.
        if reference_unit == 0:
            raise ValueError(
                "HX711::set_reference_unit_a() can't accept 0 as a reference unit!")

        self.reference_unit = reference_unit

    def set_reference_unit_b(self, reference_unit):
        # Make sure we aren't asked to use an invalid reference unit.
        if reference_unit == 0:
            raise ValueError(
                "HX711::set_reference_unit_a() can't accept 0 as a reference unit!")

        self.reference_unit_b = reference_unit

    def get_reference_unit(self):
        return self.get_reference_unit_a()

    def get_reference_unit_a(self):
        return self.reference_unit

    def get_reference_unit_b(self):
        return self.reference_unit_b

    def power_down(self):
        # Wait for and get the Read Lock, incase another thread is already
        # driving the HX711 serial interface.
        self.read_lock.acquire()

        # Cause a rising edge on HX711 Digital Serial Clock (pd_sck).  We then
        # leave it held up and wait 100 us.  After 60us the HX711 should be
        # powered down.
        GPIO.output(self.pd_sck, False)
        GPIO.output(self.pd_sck, True)

        time.sleep(0.0001)

        # Release the Read Lock, now that we've finished driving the HX711
        # serial interface.
        self.read_lock.release()

    def power_up(self):
        # Wait for and get the Read Lock, incase another thread is already
        # driving the HX711 serial interface.
        self.read_lock.acquire()

        # Lower the HX711 Digital Serial Clock (pd_sck) line.
        GPIO.output(self.pd_sck, False)

        # Wait 100 us for the HX711 to power back up.
        time.sleep(0.0001)

        # Release the Read Lock, now that we've finished driving the HX711
        # serial interface.
        self.read_lock.release()

        # HX711 will now be defaulted to Channel A with gain of 128.  If this
        # isn't what client software has requested from us, take a sample and
        # throw it away, so that next sample from the HX711 will be from the
        # correct channel/gain.
        if self._get_gain() != 128:
            self._read_raw_bytes()

    def reset(self):
        self.power_down()
        self.power_up()
