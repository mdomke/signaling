
``signaling`` slots with signals
================================


Signaling is a Python library that provides a simple implementation of the 
`signal/slot pattern`_ best known from the `Qt framework`_. It allows you to
implement object-to-object and broadcast signaling.

Examples
--------

.. module:: signaling

Connecting signals
~~~~~~~~~~~~~~~~~~

To connect a signal to a slot (receiver) use the :meth:`Signal.connect()`-method.

.. code-block:: python
  
  def receiver(count):
    print("Got triggered with {}".format(count))

  signal = Signal(args=['count'])
  signal.connect(receiver)


Emiting Signals
~~~~~~~~~~~~~~~

To notify receivers about events, use the :meth:`Signal.emit()` method.

.. code-block:: python

  signal.emit(count=1)  # Got triggered with 1


Validation
----------

The ``signaling`` library performs some sanity checks when connecting slots and
emitting signals in order to prevent programming errors.

* All slots connected to a signal have to provide the same argument specifiction as
  denoted by the ``args`` parameter of the :class:`Signal` constructor.
* An :meth:`Signal.emit()`-call has to be made with the exact same arguments as
  specified with the :class:`Signal` constructor.

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


API documentation
-----------------

.. toctree::
   :maxdepth: 2

   api

.. _qt framework: http://www.qt.io/
.. _signal/slot pattern: https://en.wikipedia.org/wiki/Signals_and_slots
