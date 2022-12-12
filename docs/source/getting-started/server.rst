Creating a server
=================

Instantiating the server class
------------------------------

You can instantiate the server class with :py:class:`socketsc.SocketServer`.
It takes 3 parameters:


.. py:data:: address
        :noindex:

        A tuple with the address and port to bind to

.. py:data:: address_family
        :noindex:

        The address family to use, :py:data:`socketsc.AF_INET` or :py:data:`socketsc.AF_INET6`

.. py:data:: sock_type
        :noindex:

        The socket type to use, :py:data:`socketsc.SOCK_TCP`, UDP not supported yet

.. literalinclude:: ../code_examples/server.py
    :lines: 1-4


Registering an event
--------------------

You can register an event through the :py:data:`socketsc.SocketServer.on` method. It takes 2 parameters:

.. py:data:: event_name
        :noindex:

        The name of the event to register

.. py:data:: event_exec
        :noindex:

        The function to execute when the event is triggered

.. literalinclude:: ../code_examples/server.py
    :lines: 7-13

The function that you pass to the :py:data:`socketsc.SocketServer.on` method will be called like this:

.. py:function:: on_event(client, data)
    :noindex:

    The callback function that will be executed when the event is triggered.

    :param client: The client connection object :py:class:`socketsc.ServerSocketWrapper`
    :param data: The data sent by the client


Starting the server
-------------------

Now that we have registered our event, we can start the server with the :py:data:`socketsc.SocketServer.serve` method.

.. literalinclude:: ../code_examples/server.py
    :lines: 15-17

The server will now listen for incoming connections and execute the callback function when the events are triggered.


Full code
---------

.. literalinclude:: ../code_examples/server.py

Learn more
----------

- :doc:`Library references <../references/index>`