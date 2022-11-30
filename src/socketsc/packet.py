import struct
import json
from .utils import recvall

__all__ = [
    "SocketPacket",
    "SocketPacketData"
]


class SocketPacketData:
    """
    Class for data returned by `SocketPacket.unpack()`
    """
    def __init__(self, event, data):
        self.event = event
        self.data = data


class SocketPacket:
    """
    Class for encoding and decoding socket packets
    Socket packet format:
        - 4 bytes: event length
        - event name
        - 4 bytes: data type length
        - data type
        - 4 bytes: data length
        - data
    """
    def __init__(self, event, data):
        self.event = event
        self.data = data

    def pack(self):
        """
        Pack the packet into bytes. See `SocketPacket` for packet format
        :return: bytes
        """
        encoded_data = SocketPacket.encode_data(self.data)

        return (
            struct.pack(">I", len(self.event))
            + self.event.encode()
            + struct.pack(">I", len(encoded_data[0]))
            + encoded_data[0]
            + struct.pack(">I", len(encoded_data[1]))
            + encoded_data[1]
        )

    @staticmethod
    def encode_data(data):
        """
        Encode data to bytes
        :param data: The data to encode
        :return: A tuple of the data type and the encoded data
        :raises TypeError: If the data type is not supported
        """
        try:
            return b"json", json.dumps(data).encode()
        except TypeError:
            pass

        data_type = type(data)
        if data_type == bytes:
            return b"bytes", data
        elif data_type == bytearray:
            return b"barray", data
        else:
            raise TypeError(f"Unknown data type: {data_type}")

    @staticmethod
    def decode_data(data_type, data):
        """
        Decode data from bytes
        :param data_type: The data type
        :param data: The data to decode
        :return: The decoded data
        :raises TypeError: If the data type is not supported
        """
        if data_type == b"json":
            return json.loads(data)
        elif data_type == b"bytes":
            return data
        elif data_type == b"barray":
            return bytearray(data)
        else:
            raise TypeError(f"Unknown data type: {data_type}")

    @staticmethod
    def unpack(sock):
        """
        Unpack data received from a socket
        :param sock: The socket to receive data from
        :return: A `SocketPacketData` object
        """
        raw_event_len = recvall(sock, 4)
        if not raw_event_len:
            return None
        event_len = struct.unpack(">I", raw_event_len)[0]
        event = recvall(sock, event_len).decode()
        raw_data_type_len = recvall(sock, 4)
        if not raw_data_type_len:
            return None
        data_type_len = struct.unpack(">I", raw_data_type_len)[0]
        data_type = recvall(sock, data_type_len)

        raw_data_len = recvall(sock, 4)
        if not raw_data_len:
            return None
        data_len = struct.unpack(">I", raw_data_len)[0]
        data = recvall(sock, data_len)

        decoded_data = SocketPacket.decode_data(data_type, data)

        return SocketPacketData(event, decoded_data)
