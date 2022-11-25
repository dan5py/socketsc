import socket
import threading
import socketsc.constants as constants
from socketsc.Client.ClientEventManager import ClientEventManager
import json


class SocketClient:
    """
    Socket client.
    """
    def __init__(self, server_address, socket_family, sock_type):
        self.server_address = server_address
        self.socket_family = socket_family
        self.sock_type = sock_type
        self.socket = socket.socket(self.socket_family, self.sock_type)
        self.event_manager = ClientEventManager()
        self.connected = False
        self.connection_event = threading.Event()
        self.thread = threading.Thread(target=self.connect)
        self.thread.start()

    def connect(self):
        self.socket.connect(self.server_address)
        self.connection_event.set()
        self.connected = True
        while True:
            data = self.socket.recv(constants.BUFFER_SIZE)
            if not data:
                break
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
        self.socket.sendall(json_data.encode("utf-8"))

    def on(self, event, callback):
        """
        Register an event
        :param event: The event name
        :param callback: The function to register
        :return:
        """
        self.event_manager.add_event(event, callback)
