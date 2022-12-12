import socketsc

# Instantiate the client
server = socketsc.SocketClient(("localhost", 8080), socketsc.AF_INET, socketsc.SOCK_TCP)


def on_answer(conn: socketsc.SocketClient, answer):
    # Callback function for the "answer" event
    print(f"Server answered: {answer}")


# Register an event
server.on("answer", on_answer)

# Emit the event with the data
server.emit("question", "Are you there server?")
