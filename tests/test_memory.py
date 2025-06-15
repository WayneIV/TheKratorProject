from krator.modules.context_memory import ContextMemory


def test_add_and_recall():
    mem = ContextMemory(max_events=2)
    mem.add_event('type', 'data1')
    mem.add_event('type', 'data2')
    mem.add_event('type', 'data3')
    events = mem.recall()
    assert len(events) == 2
    assert events[0][1] == 'data2'
    assert events[1][1] == 'data3'
