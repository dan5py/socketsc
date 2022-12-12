Creating a client
=================


Instantiating the client class
------------------------------

Just like the server you can instantiate the client class with :py:class:`socketsc.SocketClient`.
It takes 3 parameters:

.. py:data:: address
        :noindex:

        A tuple with the address and port of the server

.. py:data:: address_family
        :noindex:

        The address family to use, :py:data:`socketsc.AF_INET` or :py:data:`socketsc.AF_INET6`

.. py:data:: sock_type
        :noindex:

        The socket type to use, :py:data:`socketsc.SOCK_TCP`, UDP not supported yet

.. literalinclude:: ../code_examples/client.py
    :lines: 1-4

Registering an event
--------------------

You can register an event through the :py:data:`socketsc.SocketClient.on` method. It takes 2 parameters:

.. py:data:: event_name
        :noindex:

        The name of the event to register

.. py:data:: event_exec
        :noindex:

        The function to execute when the event is triggered

.. literalinclude:: ../code_examples/client.py
    :lines: 7-13

The function that you pass to the :py:data:`socketsc.SocketClient.on` method will be called like this:

.. py:function:: on_event(client, data)
    :noindex:

    The callback function that will be executed when the event is triggered.

    :param client: The client connection object :py:class:`socketsc.SocketClient`
    :param data: The data sent by the client

Emitting an event
-----------------

You can emit an event through the :py:data:`socketsc.SocketClient.emit` method. It takes 2 parameters:

.. py:data:: event_name
        :noindex:

        The name of the event to emit

.. py:data:: data
        :noindex:

        The data to send to the server. Accepts any ``json serializable data`` and ``bytes``.

.. literalinclude:: ../code_examples/client.py
    :lines: 15-16


Full code
---------

.. literalinclude:: ../code_examples/client.py

Learn more
----------

Check out how to remove an event in the :doc:`next section <removelisteners>`.

- :doc:`Library references <../references/index>`