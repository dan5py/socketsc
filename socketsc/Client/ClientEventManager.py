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
