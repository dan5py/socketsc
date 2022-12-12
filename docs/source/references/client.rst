Client
======

.. py:currentmodule:: socketsc

.. py:class:: SocketClient

    The socket client class.

    :param address: A tuple with the address and port of the server.
    :param address_family: The address family to use (:py:data:`socketsc.socket.AF_INET` or :py:data:`socketsc.AF_INET6`)
    :param sock_type: The socket type to use (Only :py:data:`socketsc.SOCK_TCP` is supported at the moment)

    :ivar connected: A boolean indicating if the client is connected to the server.

    :returns: A :py:class:`SocketClient` object.

    .. py:method:: connect()

        Connect to the server and start listening for incoming messages.

    .. py:method:: on(event, callback)

        Register a callback for an event.

        :param str event: The event to listen for.
        :param Callable[SocketClient, Any] callback: The callback to call when the event is received.

    .. py:method:: emit(event, data=None)

        Emit an event to the server.

        :param str event: The event to emit.
        :param Any data: The data to send.

    .. py:method:: remove_listener(event, callback)

        Remove a listener for a specific event

        :param str event: The event to remove the listener for
        :param Callable[SocketClient, Any] callback: The callback to remove

    .. py:method:: remove_all_listeners(event)

        Remove all listeners for a specific event

        :param str event: The event to remove all listeners for

    .. py:method:: shutdown(__how)

        Shutdown the socket.

        :param int __how: The shutdown mode. See :ref:`address-family` for more information.

    ..  py:method:: close()

        Close the socket.