!["socketsc"](https://i.imgur.com/aVhWeoh.png)

[![License](https://img.shields.io/pypi/l/socketsc)](https://pypi.org/project/socketsc/)
[![Version](https://img.shields.io/pypi/v/socketsc)](https://pypi.org/project/socketsc/)
[![Python](https://img.shields.io/pypi/pyversions/socketsc)](https://pypi.org/project/socketsc/)
[![Downloads](https://img.shields.io/pypi/dm/socketsc)](https://pypi.org/project/socketsc/)
[![Issues](https://img.shields.io/gitlab/issues/open/dan5py/socketsc)](https://gitlab.com/dan5py/socketsc/-/issues)

## Installation

```bash
pip install socketsc
```

## Usage

Simple client and server implementation.

### Server

```python
import socketsc

server = socketsc.SocketServer(("localhost", 8080), address_family=socketsc.AF_INET, sock_type=socketsc.SOCK_TCP)

print("Server listening on port 8080")

def on_question(socket: socketsc.ServerSocketWrapper, data):
    print(f"Received {data} from {socket.client_address}")
    socket.emit("answer", "1")

server.on("question", on_question)
server.serve()
```

### Client

```python
import socketsc

server_address = ("localhost", 8080)
sock = socketsc.SocketClient(server_address, address_family=socketsc.AF_INET, sock_type=socketsc.SOCK_TCP)


def on_answer(conn: socketsc.SocketClient, data):
    print(f"Server responded with {data}")


sock.emit("question", "0")
sock.on("answer", on_answer)
```
