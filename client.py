import socketsc

server_address = ("localhost", 8080)
sock = socketsc.SocketClient(server_address, address_family=socketsc.AF_INET, sock_type=socketsc.SOCK_TCP)


def on_answer(conn: socketsc.SocketClient, data):
    print(f"Server responded with {data}")


def on_broadcast(conn: socketsc.SocketClient, data):
    print(f"Server broadcasted {data}")


sock.on("broadcast", on_broadcast)
sock.on("answer", on_answer)

sock.emit("question", input("Insert the question: "))