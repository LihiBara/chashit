"""
author - lihi
date   - 29 / 05 / 23
server
"""
#file name CashitServer.py
import socket
import threading
from CashitDB import CashitDB
import os
import base64
import simplejson as json
import config
import hashlib
import io
from cryptography.fernet import Fernet

dict = {}

class CashitServer:
    def __init__(self, host=config.SERVER_HOST_IP, port=config.SERVER_PORT):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Cashit_db = CashitDB()
        self.Cashit_db.create_tables()
        self.key = Fernet.generate_key()
        with io.open("key.key", mode='wb') as file:
            # Write content to the file
            file.write(self.key)

        self.fernet = Fernet(self.key)

    def handle_client(self, conn, addr):
        """
        a function that is connecting to each client, handeling the commands from the
        clients and decrypting it, returns an answer to them.
        :param conn:
        :param addr:
        :return:
        """
        print(f"[SERVER] New connection from {addr}.")

        while True:
            print("here")
            data = self.fernet.decrypt(conn.recv(config.PACKET_SIZE)).decode('utf-8')
            print("data", data)
            if not data:
                break

            command, args = json.loads(data)
            command = command[len(config.COMMANDPRO):]
            print(f"[SERVER] Received command '{command}' with args {args} from {addr}.")
            if command == "validate":
                username, password = args
                dict[username] = conn
                print(dict)
                response = self.Cashit_db.validate_user(username, password)
                #plen = len(response)
                #response = f"{plen}#{response}"

            elif command == "UserExist":
                username = args
                response = self.Cashit_db.user_exist(username)
                plen = len(response)
                response = str(plen) + '#' + response

            elif command == "SaveSignupDetails":
                username, password, email, id, sum = args
                self.Cashit_db.save_user(username, password, email, id, sum)
                response = True  # or any other value to indicate success

            elif command == "ReadSignup":
                username = args[0]
                user_data = self.Cashit_db.get_user(username)
                user_data = user_data
                response = user_data
                plen = len(response)
                response = str(plen) + '#' + response

            elif command == "permission":
                username, amount, second_user = args
                socket = dict[second_user]

                encryped = self.fernet.encrypt(json.dumps(f"do you agree to recieve {amount} money from {username}").encode('utf-8'))
                socket.send(encryped)
                response = json.loads(self.fernet.decrypt(socket.recv(200000000)).decode('utf-8'))

            encryped_response = self.fernet.encrypt(json.dumps(response).encode('utf-8'))
            conn.send(encryped_response)
        print(f"[SERVER] Connection with {addr} closed.")
        conn.close()

    def start(self):
        """
        a function that starts the server and listening to connections from a client by threading
        :return:
        """
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"[SERVER] Server started on {self.host}:{self.port}.")

        while True:
            conn, addr = self.server.accept()
            print("conn, addr", conn, addr)
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[SERVER] Active connections: {threading.active_count() - 1}")


if __name__ == "__main__":
    Cashit_server = CashitServer()
    Cashit_server.start()
