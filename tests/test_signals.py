import mock
import pytest

from signaling.exceptions import InvalidEmit
from signaling.exceptions import InvalidSlot
from signaling import Signal


class Receiver(object):

    def __init__(self):
        self.m = mock.Mock()

    def slot(self):
        self.m()


class TestSignalSlot(object):

    def setup_method(self, method):
        self.signal = Signal(name='emitter')
        self.sentinel_a = mock.Mock()
        self.sentinel_b = mock.Mock()

    def slot_a(self):
        self.sentinel_a()

    def slot_b(self):
        self.sentinel_b()

    def test_connect(self):
        self.signal.connect(self.slot_a)
        assert self.slot_a in self.signal.slots

        self.signal.connect(self.slot_b)
        assert self.slot_a in self.signal.slots
        assert self.slot_b in self.signal.slots

    def test_connect_with_incompatible_slot_arg_count(self):
        def slot_a():
            pass

        with pytest.raises(InvalidSlot):
            Signal(args=['foo']).connect(slot_a)

        def slot_b(foo):
            pass

        with pytest.raises(InvalidSlot):
            Signal().connect(slot_b)

    def test_connect_with_incompatible_slot_arg_name(self):
        def slot(foo):
            pass

        with pytest.raises(InvalidSlot):
            Signal(args=['bar']).connect(slot)

    def test_disconnect(self):
        self.test_connect()
        self.signal.disconnect(self.slot_a)
        assert self.slot_a not in self.signal.slots
        assert self.slot_b in self.signal.slots

        self.signal.disconnect(self.slot_b)
        assert self.slot_a not in self.signal.slots
        assert self.slot_b not in self.signal.slots

    def test_emit_with_one_slot(self):
        self.signal.connect(self.slot_a)
        self.signal.emit()
        self.sentinel_a.assert_called_once_with()
        assert self.sentinel_b.call_count == 0

    def test_emit_with_two_slots(self):
        self.signal.connect(self.slot_a)
        self.signal.connect(self.slot_b)
        self.signal.emit()
        self.sentinel_a.assert_called_once_with()
        self.sentinel_b.assert_called_once_with()

    def test_emit_with_args(self):
        def slot(foo, bar):
            self.sentinel_a(foo=foo, bar=bar)

        signal = Signal(args=['foo', 'bar'])
        signal.connect(slot)
        signal.emit(foo=1, bar=2)
        self.sentinel_a.assert_called_once_with(foo=1, bar=2)

    def test_emit_with_missing_args(self):
        def slot(foo, bar):
            self.sentinel_a(foo, bar)

        signal = Signal(args=['foo', 'bar'])
        signal.connect(slot)
        with pytest.raises(InvalidEmit):
            signal.emit(foo=1)
        self.sentinel_a.assert_not_called()

    def test_emit_with_superfluous_args(self):
        def slot(foo):
            self.sentinel_a(foo)

        signal = Signal(args=['foo'])
        signal.connect(slot)
        with pytest.raises(InvalidEmit):
            signal.emit(foo=1, bar=2)
        self.sentinel_a.assert_not_called()

    def test_emit_with_superfluous_args_none_expected(self):
        def slot():
            self.sentinel_a()

        signal = Signal()
        signal.connect(slot)
        with pytest.raises(InvalidEmit):
            signal.emit(foo=1)
        self.sentinel_a.assert_not_called()

    def test_emit_with_method_slot(self):
        signal = Signal()
        receiver = Receiver()
        signal.connect(receiver.slot)
        signal.emit()
        receiver.m.assert_called_with()

    def test_repr(self):
        signal = Signal()
        assert repr(signal) == u"<Signal: 'anonymous'. Slots=0>"
        signal.connect(self.slot_a)
        assert repr(signal) == u"<Signal: 'anonymous'. Slots=1>"

    def test_equality(self):
        other = Signal()
        assert self.signal == other
        self.signal.connect(self.slot_a)
        assert self.signal != other
