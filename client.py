import socketsc

server_address = ("localhost", 8080)
sock = socketsc.SocketClient(server_address, socket_family=socketsc.AF_INET, sock_type=socketsc.SOCK_TCP)


def on_answer(conn: socketsc.SocketClient, data):
    print(f"Server responded with {data}")


sock.emit("question", input("Insert the question: "))
sock.on("answer", on_answer)