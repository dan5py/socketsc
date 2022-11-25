import socketserver
import socketsc.constants
from socketsc.Server.SocketTCPRequestHandler import SocketTCPRequestHandler
from socketsc.Server.SocketUDPRequestHandler import SocketUDPRequestHandler
from socketsc.Server.ClientManager import ClientManager
from socketsc.Server.ServerEventManager import ServerEventManager


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


# class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
#     """
#         UDP Socket server that implement threads for client connections.
#     """
#     event_manager = ServerEventManager()
#
#     def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
#         super().__init__(server_address, RequestHandlerClass, bind_and_activate)


class SocketServer:
    """
    Socket server wrapper.
    """
    server: ThreadedTCPServer
    daemon_threads = True

    def __init__(
        self,
        address,
        sock_type,
        address_family,
    ):
        if sock_type != socketsc.constants.SOCK_TCP:  # and sock_type != self.SOCK_UDP:
            raise ValueError("Unsupported socket type")
        # handler = SocketTCPRequestHandler if sock_type == socketsc.constants.SOCK_TCP else SocketUDPRequestHandler
        handler = SocketTCPRequestHandler
        # if sock_type == socketsc.constants.SOCK_TCP:
        self.server = ThreadedTCPServer(address, address_family, handler, True, self.daemon_threads)
        # elif sock_type == socketsc.constants.SOCK_UDP:
        #     self.server = ThreadedUDPServer(address, handler)

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