import socket
import threading
import queue

# Create a thread-safe message queue
message_queue = queue.Queue()

# List of connected clients (listeners)
listeners = []

# Function to handle client connections (Publisher or Listener)
def handle_client(client_socket, addr):
    global listeners
    while True:
        try:
            # Receive data from the client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            # Check if the client is a publisher or listener
            if message.startswith("PUT"):
                # Example: PUT:Your message here
                _, msg = message.split(":", 1)
                message_queue.put(msg)
                client_socket.send("Message added to the queue.\n".encode('utf-8'))
                # Notify all listeners
                notify_listeners(msg)
            elif message == "LISTEN":
                # Add client to the listener list
                listeners.append(client_socket)
                client_socket.send("You are now listening for messages.\n".encode('utf-8'))
            else:
                client_socket.send("Invalid command. Use PUT or LISTEN.\n".encode('utf-8'))
        except ConnectionResetError:
            break

    client_socket.close()

# Function to notify all listeners when a new message is published
def notify_listeners(message):
    global listeners
    for listener in listeners:
        try:
            listener.send(f"New message: {message}\n".encode('utf-8'))
        except:
            listeners.remove(listener)

# Function to start the server
def start_server(host='127.0.0.1', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")

        # Handle client connection in a new thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
