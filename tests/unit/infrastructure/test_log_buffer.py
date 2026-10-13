from app.infrastructure.log_buffer import LogBuffer
from tests.fixtures.ui import UpdateSpy


def test_append_and_take_snapshot(log_buffer):
    log_buffer.append("INFO", "First log")
    log_buffer.append("ERROR", "Second log")
    snapshot = log_buffer.take_snapshot()

    assert len(snapshot) == 2
    assert snapshot == [("INFO", "First log"), ("ERROR", "Second log")]


def test_snapshot_returns_copy(log_buffer):
    log_buffer.append("INFO", "Log entry")
    snapshot = log_buffer.take_snapshot()
    snapshot.clear()

    assert len(log_buffer.take_snapshot()) == 1


def test_capacity_eviction():
    buffer = LogBuffer(maxlen=3)
    buffer.append("INFO", "Log 1")
    buffer.append("INFO", "Log 2")
    buffer.append("INFO", "Log 3")
    buffer.append("INFO", "Log 4")
    snapshot = buffer.take_snapshot()

    assert len(snapshot) == 3
    assert snapshot[0] == ("INFO", "Log 2")
    assert snapshot[-1] == ("INFO", "Log 4")


def test_listener_notification_on_append(log_buffer):
    listener = UpdateSpy()
    log_buffer.subscribe(listener)
    log_buffer.append("WARNING", "Test warning")

    listener.assert_called_once()


def test_unsubscribe_listener(log_buffer):
    listener = UpdateSpy()
    log_buffer.subscribe(listener)
    log_buffer.unsubscribe(listener)
    log_buffer.append("INFO", "Test message")

    listener.assert_not_called()


def test_clear_buffer_notifies_listeners(log_buffer):
    listener = UpdateSpy()
    log_buffer.subscribe(listener)
    log_buffer.append("INFO", "Log before clear")
    listener.called = False
    listener.call_count = 0
    log_buffer.clear()

    assert len(log_buffer.take_snapshot()) == 0
    listener.assert_called_once()
