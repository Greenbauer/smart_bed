from smart_bed.status import save, get


REAL_STATUS = get()


def restore_status():
    save(REAL_STATUS)


def light_state_checker(current_state, end_state):
    # give a +- 1 range of allowed values, because the float to int conversion is a little off
    for i, val in enumerate(end_state):
        current = current_state[i]

        assert val <= current + 1 >= current - 1
