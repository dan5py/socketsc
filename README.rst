.. image:: https://i.imgur.com/aVhWeoh.png
    :alt: socketsc

------------

|license| |version| |pyversion| |downloads| |issues|

.. |license| image:: https://img.shields.io/pypi/l/socketsc
   :target: https://pypi.org/project/socketsc/
   :alt: PyPI - License

.. |version| image:: https://img.shields.io/pypi/v/socketsc
   :target: https://pypi.org/project/socketsc/
   :alt: PyPi - Version

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/socketsc
   :target: https://pypi.org/project/socketsc/
   :alt: PyPI - Python Version

.. |downloads| image:: https://img.shields.io/pypi/dm/socketsc
   :target: https://pypi.org/project/socketsc/
   :alt: PyPI - Downloads

.. |issues| image:: https://img.shields.io/gitlab/issues/open/dan5py/socketsc
   :target: https://gitlab.com/dan5py/socketsc/-/issues
   :alt: GitLab issues


A simple socket library with events management.

Installation
------------

.. code-block:: bash

    pip install socketsc

Usage
-----

Simple client and server implementation.

Server
~~~~~~

.. code-block:: python

    import socketsc

    server = socketsc.SocketServer(("localhost", 8080), address_family=socketsc.AF_INET, sock_type=socketsc.SOCK_TCP)

    print("Server listening on port 8080")

    def on_question(socket: socketsc.ServerSocketWrapper, data):
        print(f"Received {data} from {socket.client_address}")
        socket.emit("answer", "1")

    server.on("question", on_question)
    server.serve()

Client
~~~~~~

.. code-block:: python

    import socketsc

    server_address = ("localhost", 8080)
    sock = socketsc.SocketClient(server_address, address_family=socketsc.AF_INET, sock_type=socketsc.SOCK_TCP)


    def on_answer(conn: socketsc.SocketClient, data):
        print(f"Server responded with {data}")


    sock.emit("question", "0")
    sock.on("answer", on_answer)