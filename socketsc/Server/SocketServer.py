import socketserver
import socketsc.constants
from socketsc.Server.SocketTCPRequestHandler import SocketTCPRequestHandler
from socketsc.Server.SocketUDPRequestHandler import SocketUDPRequestHandler
from socketsc.Server.ClientManager import ClientManager
from socketsc.Server.ServerEventManager import ServerEventManager


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    TCP Socket server that implement threads for client connections.
    """
    client_manager = ClientManager()
    event_manager = ServerEventManager()

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    """
        UDP Socket server that implement threads for client connections.
    """
    event_manager = ServerEventManager()

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)


class SocketServer:
    """
    Socket server wrapper.
    """
    server: ThreadedTCPServer

    def __init__(
        self,
        address,
        sock_type,
    ):
        if sock_type != socketsc.constants.SOCK_TCP:  # and sock_type != self.SOCK_UDP:
            raise ValueError("Invalid socket type")
        # handler = SocketTCPRequestHandler if sock_type == socketsc.constants.SOCK_TCP else SocketUDPRequestHandler
        handler = SocketTCPRequestHandler
        # if sock_type == socketsc.constants.SOCK_TCP:
        self.server = ThreadedTCPServer(address, handler)
        # elif sock_type == socketsc.constants.SOCK_UDP:
        #     self.server = ThreadedUDPServer(address, handler)

    def serve(self):
        self.server.serve_forever()

    def on(self, event_name, event_exec):
        self.server.event_manager.add_event(event_name, event_exec)