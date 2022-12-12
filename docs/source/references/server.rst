Server
======

.. py:currentmodule:: socketsc

.. py:class:: SocketServer

    The socket server class.

    :param address: A tuple with the address and port to bind to
    :param address_family: The address family to use (:py:data:`socketsc.AF_INET` or :py:data:`socketsc.AF_INET6`)
    :param sock_type: The socket type to use (Only :py:data:`socketsc.SOCK_TCP` is supported at the moment)

    :returns: A :py:class:`SocketServer` instance

    .. py:method:: serve()

        Start the server

    .. py:method:: on(event, callback)

        Register a callback for a specific event

        :param str event: The event to register the callback for
        :param Callable[ServerSocketWrapper, Any] callback: The callback to register

    .. py:method:: emit(event, data=None)

        Emit an event to all connected clients. (Broadcast)

        :param str event: The event to emit
        :param Any data: The data to send

    .. py:method:: remove_listener(event, callback)

        Remove a listener for a specific event

        :param str event: The event to remove the listener for
        :param Callable[ServerSocketWrapper, Any] callback: The callback to remove

    .. py:method:: remove_all_listeners(event)

        Remove all listeners for a specific event

        :param str event: The event to remove all listeners for


.. py:class:: ServerSocketWrapper

    This class is used to wrap the client connection socket and provide a way register and emit events for that specific client.

    :param Client client: The client instance to wrap

    .. py:attribute:: client_address
        :type: Tuple[str, int]

        The address of the client

    .. py:attribute:: client_id
        :type: str

        The client uuid

    .. py:attribute:: connection
        :type: socket.socket

        The client connection socket

    .. py:method:: on(event, callback)

        Register a callback for a specific event

        :param str event: The event to register the callback for
        :param Callable[ServerSocketWrapper, Any] callback: The callback to register

    .. py:method:: emit(event, data)

            Emit an event to the client

            :param str event: The event to emit
            :param Any data: The data to send

    .. py:method:: remove_listener(event, callback)

            Remove a listener for a specific event

            :param str event: The event to remove the listener for
            :param Callable[ServerSocketWrapper, Any] callback: The callback to remove

    .. py:method:: remove_all_listeners(event)

            Remove all listeners for a specific event

            :param str event: The event to remove all listeners for
