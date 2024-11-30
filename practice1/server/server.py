import socket
import os

def start_server(host='127.0.0.1', port=65432, buffer_size=1024):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")

        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")

        with conn:
            while True:
                # Receive header
                header = conn.recv(buffer_size).decode().strip()
                if not header:
                    break

                # Process based on header type
                if header.startswith("TEXT"):
                    length = int(header.split(":")[1])
                    text_data = conn.recv(length).decode()
                    print(f"Received text: {text_data}")

                elif header.startswith("FILE"):
                    _, filename, filesize = header.split(":")
                    filesize = int(filesize)
                    print(f"Receiving file: {filename} ({filesize} bytes)")

                    with open(filename, 'wb') as f:
                        received = 0
                        while received < filesize:
                            data = conn.recv(buffer_size)
                            if not data:
                                break
                            f.write(data)
                            received += len(data)

                    print(f"File {filename} received successfully.")

if __name__ == "__main__":
    start_server()
