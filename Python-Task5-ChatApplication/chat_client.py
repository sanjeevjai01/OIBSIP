import socket
import threading


HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            if not message:
                break

            print("\r" + " " * 80 + "\r", end="")
            print(message)
            print("> ", end="", flush=True)

        except:
            print("\nDisconnected from server.")
            break


def start_client():

    username = input("Enter your username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        client.connect((HOST, PORT))

        client.send(username.encode("utf-8"))

        print("\n" + "=" * 50)
        print("       CHAT APPLICATION")
        print("=" * 50)
        print("Connected to the server.")
        print("Type your message and press Enter.")
        print("Type 'exit' to leave the chat.")
        print("=" * 50)

        receive_thread = threading.Thread(
            target=receive_messages,
            args=(client,)
        )

        receive_thread.daemon = True
        receive_thread.start()

        while True:

            message = input("> ").strip()

            if message.lower() == "exit":
                break

            if message:
                client.send(message.encode("utf-8"))

    except ConnectionRefusedError:
        print("\nCould not connect to the server.")
        print("Make sure chat_server.py is running first.")

    except Exception as error:
        print("\nError:", error)

    finally:
        client.close()
        print("\nChat application closed.")


if __name__ == "__main__":
    start_client()
