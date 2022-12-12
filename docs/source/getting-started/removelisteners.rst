Removing events
==========================

Sometime you might need to remove a registered event. This can be done in two ways.


Removing all callbacks of a specific event name
------------------------------------------------

This removes all the functions that have been registered to the event name.

.. code-block:: python

    def callback_1(connection, data):
        print(f"Callback 1 {data}")

    def callback_2(connection, data):
        print(f"Callback 2 {data}")
        # Remove all the callbacks of the event "test"
        server.remove_all_listeners("test")

    server.on("test", callback_1)
    server.on("test", callback_2)

When the :func:`callback_2` is called, it will remove all the callbacks of the event "test". So when the socket receives the event "test", nothing will be triggered.



Removing a specific callback
----------------------------

This removes a specific callback from the event name.

.. code-block:: python

    def callback_1(connection, data):
        print(f"Callback 1 {data}")

    def callback_2(connection, data):
        print(f"Callback 2 {data}")
        # Remove all the callbacks of the event "test"
        server.remove_listener("test", callback_1)

    server.on("test", callback_1)
    server.on("test", callback_2)

When the :func:`callback_2` is called, it will remove the callback :func:`callback_1` of the event "test". So when the socket receives the event "test", only the :func:`callback_2` will be triggered.


.. important::

    These two examples are implemented in the server but you can also use them in the client.

Learn more
----------

- :doc:`Library references <../references/index>`