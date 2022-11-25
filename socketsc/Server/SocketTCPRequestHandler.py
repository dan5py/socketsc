from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from socketsc.Server.SocketServer import ThreadedTCPServer

import socketserver
import socket
import json
from socketsc.Logger import Logger


class SocketTCPRequestHandler(socketserver.StreamRequestHandler):
    """
    The request handler for TCP socker server
    """
    def handle(self):
        server: ThreadedTCPServer = self.server
        client_manager = server.client_manager
        client_id = client_manager.add_client(self)
        Logger.info(f"Client connected from {self.client_address} with id {client_id}")
        try:
            while True:
                raw_data = self.request.recv(1024)
                if not raw_data:
                    break
                [event, data] = json.loads(raw_data.decode("utf-8"))
                server.event_manager.call_event(event, data, self)
        except (ConnectionResetError, BrokenPipeError):
            pass
        finally:
            client_manager.remove_client(client_id)
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            Logger.info(f"Client {client_id} disconnected from {self.client_address}")
