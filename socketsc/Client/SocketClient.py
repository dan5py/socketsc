import socket
import threading
import json
from socketsc.Client.ClientEventManager import ClientEventManager
from socketsc.utils import recv_msg, send_msg


class SocketClient:
    """
    Socket client.
    """

    daemon_thread = False

    def __init__(self, server_address, address_family, sock_type):
        self.server_address = server_address
        self.address_family = address_family
        self.sock_type = sock_type
        self.socket = socket.socket(self.address_family, self.sock_type)
        self.event_manager = ClientEventManager()
        self.connected = False
        self.connection_event = threading.Event()
        self.thread = threading.Thread(target=self.connect, daemon=self.daemon_thread)
        self.thread.start()

    def connect(self):
        """
        Connect to the server and start listening for events

        :return:
        """
        self.socket.connect(self.server_address)
        self.connection_event.set()
        self.connected = True
        while True:
            if not self.connected:
                break
            data = recv_msg(self.socket)
            if not data:
                continue
            [event, data] = json.loads(data.decode("utf-8"))
            self.event_manager.call_event(event, data, self)

    def emit(self, event, data):
        """
        Emit an event

        :param event: The event name
        :param data: The data to send
        :return:
        """
        self.connection_event.wait()
        json_data = json.dumps([event, data])
        send_msg(self.socket, json_data.encode("utf-8"))

    def on(self, event, callback):
        """
        Register an event

        :param event: The event name
        :param callback: The function to register
        :return:
        """
        self.event_manager.add_event(event, callback)

    def remove_listener(self, event, callback):
        """
        Remove a listener for the given event

        :param event: The event name
        :param callback: The function to remove
        :return:
        """
        self.event_manager.remove_listener(event, callback)

    def remove_all_listeners(self, event):
        """
        Remove all listeners for the given event

        :param event: The event name
        :return:
        """
        self.event_manager.remove_all_listeners(event)

    def close(self):
        """
        Close the socket
        :return:
        """
        self.connected = False
        self.socket.close()
