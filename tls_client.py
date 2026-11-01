
import socket
import ssl

HOST = "127.0.0.1"
PORT = 5002


def run_client():
    # Create TLS context and trust our lab CA
    context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH,
        cafile="ca.crt"
    )

    # Compatibility adjustment for our lab CA certificate
    context.verify_flags &= ~ssl.VERIFY_X509_STRICT

    try:
        # Create TCP connection and wrap it with TLS
        with socket.create_connection(
            (HOST, PORT), timeout=10
        ) as sock:

            with context.wrap_socket(
                sock, server_hostname="localhost"
            ) as tls_connection:

                print("Secure TLS connection established!")
                print("TLS version:", tls_connection.version())

                # Ask the user for a message
                message = input("Enter your message: ")

                if not message.strip():
                    print("Message cannot be empty.")
                    return

                # Send message to the server
                tls_connection.sendall(message.encode("utf-8"))

                # Receive server response
                response = tls_connection.recv(1024).decode("utf-8")
                print("Server response:", response)

    except ssl.SSLCertVerificationError as error:
        print("Certificate verification failed:", error)

    except ssl.SSLError as error:
        print("TLS error:", error)

    except (ConnectionRefusedError, TimeoutError, OSError) as error:
        print("Connection error:", error)


if __name__ == "__main__":
    run_client()
