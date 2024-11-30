import socket
import os

def send_text(message, host='127.0.0.1', port=65432, buffer_size=1024):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # Send text header and message
        header = f"TEXT:{len(message)}"
        client_socket.sendall(header.encode())
        client_socket.sendall(message.encode())

        print("Text sent successfully.")

def send_file(file_path, host='127.0.0.1', port=65432, buffer_size=1024):
    if not os.path.exists(file_path):
        print("File does not exist!")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # Prepare file header
        filename = os.path.basename(file_path)
        filesize = os.path.getsize(file_path)
        header = f"FILE:{filename}:{filesize}"
        client_socket.sendall(header.encode())

        # Send file content
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                client_socket.sendall(data)

        print(f"File {filename} sent successfully.")

if __name__ == "__main__":
    mode = input("Enter mode (text/file): ").strip().lower()
    if mode == "text":
        message = input("Enter the text to send: ").strip()
        send_text(message)
    elif mode == "file":
        file_path = input("Enter the file path to send: ").strip()
        send_file(file_path)
    else:
        print("Invalid mode!")
