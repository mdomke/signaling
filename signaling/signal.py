import inspect

from signaling.exceptions import InvalidEmit
from signaling.exceptions import InvalidSlot


class Signal(object):

    def __init__(self, args=None, name=None):
        self.slots = []
        self.name = name
        self.args = args

    def emit(self, **kwargs):
        """Emit signal by calling all connected slots.

        The arguments supplied have to match the signal definition.

        Args:
            kwargs: Keyword arguments to be passed to connected slots.

        Raises:
            :exc:`InvalidEmit`: If arguments don't match signal specification.
        """
        self._ensure_emit_kwargs(kwargs)
        for slot in self.slots:
            slot(**kwargs)

    def _ensure_emit_kwargs(self, kwargs):
        if self.args and set(self.args).symmetric_difference(kwargs.keys()):
            raise InvalidEmit("Emit has to be called with args '{}'".format(self.args))
        elif not self.args and kwargs:
            raise InvalidEmit("Emit has to be called without arguments.")

    def is_connected(self, slot):
        """Check if a slot is conncted to this signal."""
        return slot in self.slots

    def connect(self, slot):
        """Connect ``slot`` to this singal.

        Args:
            slot (callable): Callable object wich accepts keyword arguments.

        Raises:
            InvalidSlot: If ``slot`` doesn't accept keyword arguments.
        """
        self._ensure_slot_args(slot)
        if not self.is_connected(slot):
            self.slots.append(slot)

    def _ensure_slot_args(self, slot):
        argspec = inspect.getargspec(slot)
        if inspect.ismethod(slot) and 'self' in argspec.args:
            argspec.args.remove('self')
        if self.args and self.args != argspec.args and not argspec.keywords:
            raise InvalidSlot("Slot '{}' has to accept args {} or "
                              "**kwargs.".format(slot.__name__, self.args))
        if not self.args and argspec.args:
            raise InvalidSlot("Slot '{}' has to be callable without "
                              "arguments".format(slot.__name__))

    def disconnect(self, slot):
        """Disconnect ``slot`` from this signal."""
        if self.is_connected(slot):
            self.slots.remove(slot)

    def __eq__(self, other):
        return self.slots == other.slots

    def __repr__(self):
        return u"<Signal: '{}'. Slots={}>".format(self.name or 'anonymous', len(self.slots))
