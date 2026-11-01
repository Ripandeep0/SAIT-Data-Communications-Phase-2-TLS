import socket
import ssl

HOST = "127.0.0.1"
PORT = 5002


def create_tls_context():
    # Create a secure TLS server context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    # Load server certificate and private key
    context.load_cert_chain(
        certfile="server.crt",
        keyfile="privateKey_S.pem"
    )

    return context


def handle_client(client_socket, address, context):
    print(f"Connection from {address}")

    try:
        # Wrap the client connection with TLS
        with context.wrap_socket(
            client_socket, server_side=True
        ) as tls_connection:

            print("TLS connection established!")
            print("TLS version:", tls_connection.version())

            # Receive client message
            message = tls_connection.recv(1024).decode("utf-8")

            if not message:
                print("Client disconnected without sending a message.")
                return

            print("Client says:", message)

            # Send response
            reply = "Hello! Secure TLS connection successful."
            tls_connection.sendall(reply.encode("utf-8"))

            print("Response sent successfully.")

    except ssl.SSLError as error:
        print("TLS error:", error)

    except OSError as error:
        print("Socket error:", error)

    finally:
        print(f"Connection with {address} closed.")


def run_server():
    context = create_tls_context()

    # Create TCP listening socket
    with socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    ) as server_socket:

        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )

        server_socket.bind((HOST, PORT))
        server_socket.listen(5)

        print(f"TLS server listening on {HOST}:{PORT}")

        try:
            while True:
                client_socket, address = server_socket.accept()

                handle_client(
                    client_socket, address, context
                )

        except KeyboardInterrupt:
            print("\nTLS server shutting down.")

        finally:
            print("Server closed.")


if __name__ == "__main__":
    run_server()
