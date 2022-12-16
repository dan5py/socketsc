Client side
-----------

.. py:data:: connect

    Fired when the client connects to the server.

    Returns: ``None``

.. py:data:: disconnect


    Fired when the client disconnects from the server.

    Returns: ``None``

.. py:data:: message

    Fired when the server emits an event to the client.

    Returns a ``tuple`` of:

        * ``event``: The name of the emitted event.
        * ``data``: The data emitted by the server.

.. py:data:: error

    Fired when an uncaught exception occurs in the client.
    If you don't handle this event, the client will raise the exception.

    Returns:

        * ``error``: The exception message.