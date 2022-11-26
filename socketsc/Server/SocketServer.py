import socketserver
import socketsc.constants
from socketsc.Server.SocketTCPRequestHandler import SocketTCPRequestHandler
from socketsc.Server.ClientManager import ClientManager
from socketsc.Server.ServerEventManager import ServerEventManager
from socketsc.Server.ServerSocketWrapper import ServerSocketWrapper
from socketsc.Logger import Logger


class _TCPServer(socketserver.TCPServer):
    """
    Custom TCP server class.
    """
    def __init__(self, server_address, address_family, RequestHandlerClass, bind_and_activate=True):
        self.address_family = address_family
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)


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
        if sock_type != socketsc.constants.SOCK_TCP:
            raise ValueError("Unsupported socket type")
        handler = SocketTCPRequestHandler
        self.server = ThreadedTCPServer(address, address_family, handler, True, self.daemon_threads)
        self.server.event_manager.add_event("connection", self.on_connection)
        self.server.event_manager.add_event("disconnect", self.on_disconnect)

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

    def emit(self, event_name, data):
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

    def on_connection(self, connection: ServerSocketWrapper, client_id,):
        """
        Called when a client connects to the server.
        """
        Logger.info(f"Client {client_id} connected from {connection.client_address}")

    def on_disconnect(self, connection: ServerSocketWrapper, client_id):
        """
        Called when a client disconnects from the server.
        """
        Logger.info(f"Client {client_id} disconnected")
