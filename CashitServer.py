#file name CashitServer.py
import socket
import threading
from CashitDB import CashitDB
import os
import base64
import simplejson as json

import config


class CashitServer:
    def __init__(self, host=config.SERVER_HOST_IP, port=config.SERVER_PORT):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Cashit_db = CashitDB()
        self.Cashit_db.create_tables()

    def handle_client(self, conn, addr):
        print(f"[SERVER] New connection from {addr}.")

        while True:
            data = conn.recv(config.PACKET_SIZE).decode('utf-8')
            if not data:
                break

            command, args = json.loads(data)
            print(f"[SERVER] Received command '{command}' with args {args} from {addr}.")

            if command == "validate":
                username, password = args
                response = self.Cashit_db.validate_user(username, password)

            elif command == "SaveSignupDetails":
                username, password, email, id, sum = args
                self.Cashit_db.save_user(username, password, email, id, sum)
                response = True  # or any other value to indicate success

            elif command == "ReadSignup":
                username = args[0]
                user_data = self.Cashit_db.get_user(username)
                # Replace the photo path with the encoded photo data in the user_data tuple
                user_data = user_data
                response = user_data


            conn.send(json.dumps(response).encode('utf-8'))

        print(f"[SERVER] Connection with {addr} closed.")
        conn.close()

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"[SERVER] Server started on {self.host}:{self.port}.")

        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[SERVER] Active connections: {threading.active_count() - 1}")


if __name__ == "__main__":
    Cashit_server = CashitServer()
    Cashit_server.start()
