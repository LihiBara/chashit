"""
author - lihi
date   - 29 / 05 / 23
bank
"""
from CashitDB import CashitDB
import socket
import threading
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 8081
import config
import json
import io
from cryptography.fernet import Fernet
# import CashitClient


# key = Fernet.generate_key()
# with io.open("key.key", mode='wb') as file:
#     # Write content to the file
#     file.write(key)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# fernet = Fernet(key)


def start():
    server.bind((host, port))
    server.listen()
    print(f"[SERVER] Server started on {host}:{port}.")

    while True:
        conn, addr = server.accept()
        print("conn, addr", conn, addr)
        thread = threading.Thread(target=lambda: handle_client(conn, addr))
        thread.start()
        print(f"[SERVER] Active connections: {threading.active_count() - 1}")


def handle_client(conn, addr):
    while True:
        print("here")
        data = conn.recv(config.PACKET_SIZE).decode('utf-8')
        print("data", data)

        username, amount, current_money = json.loads(data)
        print(f"[SERVER] Received command '{username}' with args {amount} from {current_money}.")
        # response = 10
        # conn.send(response)
        connect(username, amount, current_money)


def connect(username, amount, current_money):
    """
    Establishes a connection to the bank using socket.
    """
    try:
        client.connect(("127.0.0.1", 9000))
        print("Connected to the server.")
    except socket.error as err:
        print("Error connecting to the server:", str(err))
    try:
        amount = int(amount)
        updated_money = current_money + amount
        print("Sending JSON data :) :", json.dumps((username, amount, updated_money)))
        msg = (json.dumps((username, updated_money))).encode('utf-8')
        client.send(msg)

        response = json.loads(client.recv(20000)).decode('utf-8')
        print(response)

    except socket.error as err:
        print(str(err))

if __name__ == "__main__":
    thread1 = threading.Thread(target=start, args=())
    thread1.start()
