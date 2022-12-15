from __future__ import annotations
from typing import Callable, Any

import uuid
import socketserver
import socket

from .constants import *
from .packet import SocketPacket

__all__ = [
    'SocketServer',
    'ServerSocketWrapper',
    'ServerEventManager',
    'SocketTCPRequestHandler',
    'ClientManager',
    'ThreadedTCPServer'
]


class SocketServer:
    """
    Socket server wrapper.
    """
    server: ThreadedTCPServer
    daemon_threads = True

    def __init__(
        self,
        address,
        address_family,
        sock_type
    ):
        if sock_type != SOCK_TCP:
            raise ValueError("Unsupported socket type")
        handler = SocketTCPRequestHandler
        self.server = ThreadedTCPServer(address, address_family, handler, True, self.daemon_threads)

    def serve(self):
        """
        Start the server.

        :return:
        """
        self.server.serve_forever()

    def on(self, event_name, event_exec):
        """
        Register an event.

        :param event_name: The event name
        :param event_exec: The function to register
        :return:
        """
        self.server.event_manager.add_event(event_name, event_exec)

    def emit(self, event_name, data=None):
        """
        Emit an event to all connected clients.

        :param event_name: The event name
        :param data: The data to send
        :return:
        """
        all_clients = self.server.client_manager.get_clients()
        for client in all_clients:
            client.emit(event_name, data)

    def remove_listener(self, event_name, event_exec):
        """
        Remove a listener for the given event.

        :param event_name: The event name
        :param event_exec: The function to remove
        :return:
        """
        self.server.event_manager.remove_listener(event_name, event_exec)

    def remove_all_listeners(self, event_name):
        """
        Remove all listeners for the given event.

        :param event_name: The event name
        :return:
        """
        self.server.event_manager.remove_all_listeners(event_name)


class SocketTCPRequestHandler(socketserver.StreamRequestHandler):
    """
    The request handler for TCP socket server
    """
    def handle(self):
        server: ThreadedTCPServer = self.server
        client_manager = server.client_manager
        client_id = client_manager.add_client(self)
        client = client_manager.get_client(client_id).client
        server.event_manager.call_event("connection", client_id, client)
        try:
            while True:
                sock_packet = SocketPacket.unpack(self.request)
                if not sock_packet:
                    break
                event = sock_packet.event
                data = sock_packet.data

                # Global event
                server.event_manager.call_event(event, data, client)
                # Local event only for this client
                client.event_manager.call_event(event, data, client)
                # Global message event
                server.event_manager.call_event("message", (event, data), client)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass
        except Exception as err:
            if server.event_manager.has_event("error"):
                server.event_manager.call_event("error", err, client)
            else:
                raise err
        finally:
            client_manager.remove_client(client_id)
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
                self.connection.close()
            except OSError:
                pass
            server.event_manager.call_event("disconnect", client_id, client)


class _TCPServer(socketserver.TCPServer):
    """
    Custom TCP server class.
    """
    def __init__(self, server_address, address_family, RequestHandlerClass, bind_and_activate=True):
        self.address_family = address_family
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)


class Client:
    """
    Client wrapper.
    """
    def __init__(self, sc: SocketTCPRequestHandler, event_manager: ServerEventManager, client_id: str):
        self.sc = sc
        self.event_manager = event_manager
        self.id = client_id


class ClientManager:
    """
    Manager for client connections. Each client
    is identified with an uid.
    """
    def __init__(self):
        self.clients = {}

    def add_client(self, client: SocketTCPRequestHandler):
        """
        Add a new client.

        :param client: The client connection
        :return: The client uid
        """
        client_id = uuid.uuid4().hex
        self.clients[client_id] = Client(client, ServerEventManager(), client_id)
        return client_id

    def remove_client(self, client_id):
        """
        Remove a client.

        :param client_id: The client uid
        :return:
        """
        self.clients.pop(client_id)

    def get_client(self, client_id):
        """
        Get a connected client

        :param client_id:
        :return: The client if exists, None otherwise
        """

        if client_id in self.clients:
            return ServerSocketWrapper(self.clients[client_id])
        return None

    def get_clients(self):
        """
        Get all the connected clients

        :return: The connected clients
        """
        return [ServerSocketWrapper(client) for client in self.clients.values()]


class ServerEventManager:
    """
    Event manager for socket server.
    """
    events: dict[str, list[Callable[[ServerSocketWrapper, Any], Any]]]

    def __init__(self):
        self.events = {}

    def has_event(self, event_name: str):
        """
        Check if the given event has listeners

        :param event_name: The event name
        :return:
        """
        return event_name in self.events

    def add_event(self, event_name: str, event_exec: Callable[[ServerSocketWrapper, Any], Any]):
        """
        Register a function for an event

        :param event_name: The event name
        :param event_exec: The function to execute
        :return:
        """
        current_events: list = self.events.get(event_name, [])
        current_events.append(event_exec)
        self.events[event_name] = current_events.copy()

    def call_event(self, event_name: str, data: Any, client: Client):
        """
        Call all the functions registered on the given event

        :param event_name: The event name
        :param data: The data to pass to the functions
        :param client: The client (see Client class)
        :return:
        """
        current_events: list = self.events.get(event_name, [])
        for event in current_events:
            event(ServerSocketWrapper(client), data)

    def remove_listener(self, event_name: str, event_exec: Callable[[ServerSocketWrapper, Any], Any]):
        """
        Remove a listener for the given event

        :param event_name: The event name
        :param event_exec: The function to remove
        :return:
        """
        current_events: list = self.events.get(event_name, [])
        try:
            current_events.remove(event_exec)
        except ValueError:
            pass

        if len(current_events) == 0:
            self.remove_all_listeners(event_name)
            return

        self.events[event_name] = current_events.copy()

    def remove_all_listeners(self, event_name: str):
        """
        Remove all listeners for the given event

        :param event_name: The event name
        :return:
        """
        self.events.pop(event_name, None)


class ServerSocketWrapper:
    """
    Wrapper for SocketTCPRequestHandler.
    This class is used when an event is called on server side.
    """
    def __init__(self, client: Client):
        self.client = client

    def emit(self, event, data=None):
        """
        Emit an event to the client

        :param event: The event name
        :param data: The data to send
        :return:
        """
        self.client.sc.request.sendall(SocketPacket(event, data).pack())

    def on(self, event: str, event_exec: Callable[[ServerSocketWrapper, Any], Any]):
        """
        Register a function for an event for this client

        :param event: The event name
        :param event_exec: The function to execute
        :return:
        """
        self.client.event_manager.add_event(event, event_exec)

    def remove_listener(self, event: str, callback):
        """
        Remove a listener

        :param event: The event name
        :param callback: The function to remove
        :return:
        """
        self.client.event_manager.remove_listener(event, callback)

    def remove_all_listeners(self, event: str):
        """
        Remove all listeners

        :param event: The event name
        :return:
        """
        self.client.event_manager.remove_all_listeners(event)

    @property
    def client_address(self):
        """
        The client address of the connection
        """
        return self.client.sc.client_address

    @property
    def client_id(self):
        """
        The client id
        """
        return self.client.id

    @property
    def connection(self):
        """
        The socket connection object
        """
        return self.client.sc.connection

    def shutdown(self, __how):
        """
        Shutdown the connection

        :param __how: The shutdown mode
        :return:
        """
        self.connection.shutdown(__how)

    def close(self):
        """
        Close the connection
        """
        self.connection.close()


class ThreadedTCPServer(socketserver.ThreadingMixIn, _TCPServer):
    """
    TCP Socket server that implement threads for client connections.
    """
    client_manager = ClientManager()
    event_manager = ServerEventManager()

    def __init__(self, server_address, address_family, RequestHandlerClass, bind_and_activate=True,
                 daemon_threads=True):
        self.daemon_threads = daemon_threads
        super().__init__(server_address, address_family, RequestHandlerClass, bind_and_activate)
