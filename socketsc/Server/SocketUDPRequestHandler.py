from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from socketsc.Server.SocketServer import ThreadedUDPServer

import socketserver
import socketsc
import socket
import json
from socketsc.Logger import Logger


class SocketUDPRequestHandler(socketserver.DatagramRequestHandler):
    """
        The request handler for TCP socker server
    """
    def handle(self):
        server: ThreadedUDPServer = self.server
        Logger.info(f"Client connected from {self.client_address}")

        try:
            while True:
                raw_data = self.socket.recvfrom(socketsc.constants.BUFFER_SIZE)
                if not raw_data:
                    continue
                print(raw_data)
                # print(f"Received {event} with data {data}")
                # server.event_manager.call_event(event, data, self.socket)
                # self.socket.sendto("OK".encode("utf-8"), self.client_address)
        except (ConnectionResetError, BrokenPipeError):
            pass
        finally:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            Logger.info(f"Client disconnected from {self.client_address}")
