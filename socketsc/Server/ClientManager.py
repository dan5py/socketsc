from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from socketsc.Server.SocketTCPRequestHandler import SocketTCPRequestHandler

import uuid


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
        self.clients[client_id] = client
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
        return self.clients.get(client_id)

    def get_clients(self):
        """
        Get all the connected clients

        :return: The connected clients
        """
        return self.clients.values()