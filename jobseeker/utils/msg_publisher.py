import socket

def publish_message(message, host='127.0.0.1', port=5555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    # Send the PUT command to publish the message
    client.send(f"PUT:{message}".encode('utf-8'))
    
    # Receive confirmation from the server
    response = client.recv(1024).decode('utf-8')
    print(f"Server response: {response}")
    
    client.close()

if __name__ == "__main__":
    # Example: Publishing a message to the server
    publish_message("Hello from Publisher!")
