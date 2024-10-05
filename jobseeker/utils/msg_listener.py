import socket

def listen_for_messages(host='127.0.0.1', port=5555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    # Send the LISTEN command to start listening for messages
    client.send("LISTEN".encode('utf-8'))
    
    # Receive confirmation from the server
    response = client.recv(1024).decode('utf-8')
    print(f"Server response: {response}")
    
    # Keep listening for new messages
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(f"New message: {message}")
        except ConnectionResetError:
            print("Server connection closed.")
            break

if __name__ == "__main__":
    # Start listening for messages from the server
    listen_for_messages()
