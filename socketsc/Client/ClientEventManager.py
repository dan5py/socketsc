from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from socketsc.Client import SocketClient


class ClientEventManager:
    """
        Event manager for socket client.
    """
    events: dict[str, list[Callable[[SocketClient], Any]]]

    def __init__(self):
        self.events = {}

    def add_event(self, event_name: str, event_exec: Callable[[SocketClient], Any]):
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

