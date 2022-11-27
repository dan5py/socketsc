from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from socketsc.Server.SocketServer import ThreadedTCPServer

import socketserver
import socket
import json
from socketsc.utils import recv_msg
from socketsc.Logger import Logger


class SocketTCPRequestHandler(socketserver.StreamRequestHandler):
    """
    The request handler for TCP socker server
    """
    def handle(self):
        server: ThreadedTCPServer = self.server
        client_manager = server.client_manager
        client_id = client_manager.add_client(self)
        server.event_manager.call_event("connection", client_id, self)
        try:
            while True:
                raw_data = recv_msg(self.request)
                if not raw_data:
                    break
                [event, data] = json.loads(raw_data.decode("utf-8"))
                server.event_manager.call_event(event, data, self)
                server.event_manager.call_event("message", (event, data), self)
        except (ConnectionResetError, BrokenPipeError):
            pass
        except Exception as err:
            if server.event_manager.has_event("error"):
                server.event_manager.call_event("error", err, self)
            else:
                raise err
        finally:
            client_manager.remove_client(client_id)
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            server.event_manager.call_event("disconnect", client_id, self)
