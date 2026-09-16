import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clients = []
usernames = []


def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode("utf-8"))
            except:
                remove_client(client)


def remove_client(client):
    if client in clients:
        index = clients.index(client)
        username = usernames[index]

        clients.remove(client)
        usernames.remove(username)

        client.close()

        print(f"{username} disconnected.")
        broadcast(f"{username} left the chat.")


def handle_client(client):
    try:
        username = client.recv(1024).decode("utf-8")

        clients.append(client)
        usernames.append(username)

        print(f"{username} joined the chat.")

        client.send(
            "Connected to the chat server.".encode("utf-8")
        )

        broadcast(
            f"{username} joined the chat.",
            client
        )

        while True:
            message = client.recv(1024)

            if not message:
                break

            text = message.decode("utf-8")

            print(f"{username}: {text}")

            broadcast(
                f"{username}: {text}",
                client
            )

    except:
        pass

    finally:
        remove_client(client)


def start_server():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))
    server.listen()

    print("=" * 50)
    print("       CHAT APPLICATION SERVER")
    print("=" * 50)
    print(f"Server running on {HOST}:{PORT}")
    print("Waiting for clients...")
    print("=" * 50)

    while True:
        client, address = server.accept()

        print(f"New connection from {address}")

        thread = threading.Thread(
            target=handle_client,
            args=(client,)
        )

        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    start_server()