import socketsc

# Instantiate the server
server = socketsc.SocketServer(("localhost", 8080), socketsc.AF_INET, socketsc.SOCK_TCP)


def on_question(client: socketsc.ServerSocketWrapper, data):
    # Callback function for the "question" event
    client.emit("answer", "Hello client")


# Register an event
server.on("question", on_question)

print("Server listening on port 8080")
# Starting the server
server.serve()
