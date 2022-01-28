from smart_bed.context import update_context
from smart_bed.status import get


def test_context_update():
    update_context()

    status = get()

    assert status['context'] in ['morning', 'mid day', 'night']
