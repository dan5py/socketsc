from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from socketsc.Server.SocketTCPRequestHandler import SocketTCPRequestHandler

import json


class ServerSocketWrapper:
    """
    Wrapper for SocketTCPRequestHandler.
    This class is used when an event is called on server side.
    """
    def __init__(self, sc: SocketTCPRequestHandler):
        self.sc = sc

    def emit(self, event, data):
        """
        Emit an event

        :param event: The event name
        :param data: The data to send
        :return:
        """
        json_data = json.dumps([event, data])
        self.sc.connection.sendall(json_data.encode("utf-8"))

    @property
    def client_address(self):
        """
        The client address of the connection
        """
        return self.sc.client_address

    @property
    def connection(self):
        """
        The socket connection object
        """
        return self.sc.connection
