import socketsc.server as socketsc

server = socketsc.SocketServer(("localhost", 8080), address_family=socketsc.AF_INET, sock_type=socketsc.SOCK_TCP)

print("Server listening on port 8080")


def on_question(socket: socketsc.ServerSocketWrapper, data):
    # print(f"Received {data} from {socket.client_address}")
    # socket.emit("answer", "1")
    socket.emit("answer", input("Insert answer: "))
    # socket.connection.close()
    # socket.connection.shutdown(socketsc.SHUT_WR)
    server.emit("broadcast", "Hello")


server.on("question", on_question)
server.serve()
