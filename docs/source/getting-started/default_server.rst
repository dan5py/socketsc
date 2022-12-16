Server side
-----------
The following events are fired by default on the server side:


.. py:data:: connection

    Fired when a client connects to the server.

    Returns:

        * ``client_id``: The new client's socket UUID.

.. py:data:: disconnect

    Fired when a client disconnects from the server.

    Returns:

        * ``client_id``: The client's socket UUID.

.. py:data:: message

    Fired when a client emits an event to the server.

    Returns a ``tuple`` of:

        * ``event``: The name of the emitted event.
        * ``data``: The data emitted by the client.

.. py:data:: error

    Fired when an uncaught exception occurs in the server.
    If you don't handle this event, the server will raise the exception.

    Returns:

        * ``error``: The exception message.
