!["socketsc"](https://i.imgur.com/aVhWeoh.png)

A simple socket library with events management.

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
