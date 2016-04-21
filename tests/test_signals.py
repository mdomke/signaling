import mock
import pytest

from signaling.exceptions import InvalidEmit
from signaling import Signal


inspect_mock = mock.Mock()
inspect_mock.getargspec.return_value = type(
    'ArgSpec', (object,), {'args': ['foo'], 'keywords': None})


def set_argspec(args, keywords=None):
    inspect_mock.getargspec.return_value.args = args
    inspect_mock.getargspec.return_value.keywords = keywords


@mock.patch('signaling.signal.inspect', inspect_mock)
class TestSignalSlot(object):

    def setup_method(self, method):
        self.signal = Signal(name='emitter')
        self.slot_a = mock.Mock()
        self.slot_b = mock.Mock()

    def teardown_method(self, method):
        set_argspec(['foo'])

    def test_connect(self):
        self.signal.connect(self.slot_a)
        assert self.slot_a in self.signal.slots

        self.signal.connect(self.slot_b)
        assert self.slot_a in self.signal.slots
        assert self.slot_b in self.signal.slots

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
        self.slot_a.assert_called_once_with()
        assert self.slot_b.call_count == 0

    def test_emit_with_two_slots(self):
        self.signal.connect(self.slot_a)
        self.signal.connect(self.slot_b)
        self.signal.emit()
        self.slot_a.assert_called_once_with()
        self.slot_b.assert_called_once_with()

    def test_emit_with_args(self):
        set_argspec(['foo', 'bar'])
        signal = Signal(args=['foo', 'bar'])
        signal.connect(self.slot_a)
        signal.emit(foo=1, bar=2)
        self.slot_a.assert_called_once_with(foo=1, bar=2)

    def test_emit_with_missing_args(self):
        set_argspec(['foo', 'bar'])
        signal = Signal(args=['foo', 'bar'])
        signal.connect(self.slot_a)
        with pytest.raises(InvalidEmit):
            signal.emit(foo=1)
        assert self.slot_a.call_count == 0

    def test_emit_with_superfluous_args(self):
        signal = Signal(args=['foo'])
        signal.connect(self.slot_a)
        with pytest.raises(InvalidEmit):
            signal.emit(foo=1, bar=2)
        assert self.slot_a.call_count == 0

    def test_repr(self):
        assert repr(Signal()) == u"<Signal: 'anonymous'. Slots=0>"

    def test_equality(self):
        other = Signal()
        assert self.signal == other
        self.signal.connect(self.slot_a)
        assert self.signal != other
