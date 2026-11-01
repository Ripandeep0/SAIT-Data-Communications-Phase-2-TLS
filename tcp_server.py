import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("127.0.0.1", 5001))

server_socket.listen(1)

print("TCP Echo Server is running...")
print("Waiting for a client...")

while True:
    client_socket, client_address = server_socket.accept()

    print("Client connected:", client_address)

    data = client_socket.recv(1024)

    if not data:
        print("Client disconnected.")
        client_socket.close()
        continue

    message = data.decode()

    print("Received:", message)

    client_socket.sendall(data)

    client_socket.close()

    print("Connection closed.")