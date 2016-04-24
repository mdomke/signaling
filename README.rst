.. image:: https://img.shields.io/pypi/v/signaling.svg?style=flat-square
    :target: https://pypi.python.org/pypi/signaling
.. image:: https://img.shields.io/travis/mdomke/signaling/master.svg?style=flat-square
    :target: https://travis-ci.org/mdomke/signaling
.. image:: https://img.shields.io/pypi/l/signaling.svg?style=flat-square
    :target: https://pypi.python.org/pypi/signaling

What is this?
=============

``signaling`` is a simple implementation of the `signal/slot pattern`_ as 
known from the `Qt framework`_.
It has no external requirements and 100% test-coverage.


Installation
============

The usual

.. code-block:: bash
  
  pip install signaling


How to use it?
==============

Consider that you have a function that should be called whenever a connected signal
is emitted, as illustrated by the following code block:

.. code-block:: python

  def slot(arg):
    print("Slot called with {}".format(arg))

  signal = Signal(args=['arg'])
  signal.connect(slot)
  signal.emit(arg=1)  # Slot called with 1

In fact you can connect multiple slots to the same signal, as long as they share the
same function signature.

Notice that the ``signaling`` library performs some sanity checks when connecting
slots and emitting signals.

* All slots connected to a signal have to provide the same argument specifiction as
  denoted by the ``args`` parameter of the ``Signal`` constructor.
* An ``emit``-call has to be made with the exact same arguments as specified with the
  ``Signal`` constructor.

So all of the below examples would raise an exception:

.. code-block:: python

  def slot_with_arg(arg):
    pass

  def slot_without_arg():
    pass

  # InvalidSlot: Slot 'slot_with_arg' has to callable without arguments
  Signal().connect(slot_with_arg)  

  # InvalidSlot: Slot 'slot_without_args' has to accept args ['arg'] or **kwargs.
  Signal(args['arg']).connect(slot_without_arg)

  s = Signal()
  s.connect(slot_without_args)
  # InvalidEmit: Emit has to be called without arguments.
  s.emit(foo=1)


.. _qt framework: http://www.qt.io/
.. _signal/slot pattern: https://en.wikipedia.org/wiki/Signals_and_slots
