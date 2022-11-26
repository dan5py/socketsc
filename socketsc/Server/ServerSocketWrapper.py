from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from socketsc.Server.SocketTCPRequestHandler import SocketTCPRequestHandler

import json
from socketsc.utils import send_msg


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
        send_msg(self.sc.request, json_data.encode("utf-8"))

    def remove_listener(self, event_name: str):
        """
        Remove a listener

        :param event_name: The event name
        :return:
        """
        self.sc.server.event_manager.remove_listener(event_name)

    def remove_all_listeners(self):
        """
        Remove all listeners

        :return:
        """
        self.sc.server.event_manager.remove_all_listeners()

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
