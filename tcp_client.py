import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 5001)

try:
    client_socket.connect(server_address)

    message = input("Enter a message: ")

    if not message.strip():
        print("Message cannot be empty.")
    else:
        client_socket.sendall(message.encode())

        data = client_socket.recv(1024)

        print("Server replied:", data.decode())

except ConnectionRefusedError:
    print("Could not connect to the server.")

finally:
    client_socket.close()