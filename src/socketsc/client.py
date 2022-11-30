from __future__ import annotations
from typing import Callable, Any

import socket
import threading

from .constants import *
from .packet import SocketPacket


__all__ = [
    'SocketClient',
    'ClientEventManager',
]

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
        self.event_manager.call_event("connect", None, self)
        try:
            while True:
                if not self.connected:
                    break
                sock_packet = SocketPacket.unpack(self.socket)
                if not sock_packet:
                    break
                event = sock_packet.event
                data = sock_packet.data
                self.event_manager.call_event(event, data, self)
                self.event_manager.call_event("message", (event, data), self)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass
        except Exception as err:
            if self.event_manager.has_event("error"):
                self.event_manager.call_event("error", err, self)
            else:
                raise err
        finally:
            self.close()
            self.event_manager.call_event("disconnect", None, self)

    def emit(self, event, data=None):
        """
        Emit an event

        :param event: The event name
        :param data: The data to send
        :return:
        """
        self.connection_event.wait()
        self.socket.sendall(SocketPacket(event, data).pack())

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

    def shutdown(self, __how):
        """
        Shutdown the socket
        :param __how: The shutdown mode
        :return:
        """
        self.socket.shutdown(__how)

    def close(self):
        """
        Close the socket
        :return:
        """
        self.connected = False
        self.socket.close()


class ClientEventManager:
    """
        Event manager for socket client.
    """
    events: dict[str, list[Callable[[SocketClient, Any], Any]]]

    def __init__(self):
        self.events = {}

    def has_event(self, event_name: str):
        """
        Check if the given event has listeners

        :param event_name: The event name
        :return:
        """
        return event_name in self.events

    def add_event(self, event_name: str, event_exec: Callable[[SocketClient, Any], Any]):
        """
            Register a function for an event

            :param event_name: The event name
            :param event_exec: The function to execute
            :return:
        """
        current_events: list = self.events.get(event_name, [])
        current_events.append(event_exec)
        self.events[event_name] = current_events.copy()

    def call_event(self, event_name: str, data: Any, connection: SocketClient):
        """
            Call all the functions registered on the given event

            :param event_name: The event name
            :param data: The data to pass to the functions
            :param connection: The socket connection
            :return:
        """
        current_events: list = self.events.get(event_name, [])
        for event in current_events:
            event(connection, data)

    def remove_listener(self, event_name: str, event_exec: Callable[[SocketClient, Any], Any]):
        """
        Remove a listener for the given event

        :param event_name: The event name
        :param event_exec: The function to remove
        :return:
        """
        current_events: list = self.events.get(event_name, [])
        try:
            current_events.remove(event_exec)
        except ValueError:
            pass

        if len(current_events) == 0:
            self.remove_all_listeners(event_name)
            return

        self.events[event_name] = current_events.copy()

    def remove_all_listeners(self, event_name: str):
        """
        Remove all listeners for the given event

        :param event_name: The event name
        :return:
        """
        self.events.pop(event_name, None)
