from smart_bed.lights import set_brightness


def test_lights_brightness_low():
    state = {'values': [10, 20, 1, 255, 0, 100]}

    expected_values = [5, 10, 0, 127, 0, 50]

    new_state_values = set_brightness(state, 50)['values']

    assert new_state_values == expected_values


def test_lights_brightness_high():
    state = {'values': [10, 20, 1, 255, 0, 100]}

    expected_values = [20, 40, 2, 255, 0, 200]

    new_state_values = set_brightness(state, 200)['values']

    assert new_state_values == expected_values
