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
dict2 = {}


class CashitServer:
    def __init__(self, host=config.SERVER_HOST_IP, port=config.SERVER_PORT):
        self.host = host
        self.port = port
        self.port2 = config.SERVER_PORT2
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Cashit_db = CashitDB()
        self.Cashit_db.create_tables()
        self.key = Fernet.generate_key()
        with io.open("key.key", mode='wb') as file:
            # Write content to the file
            file.write(self.key)

        self.fernet = Fernet(self.key)

    def handle_client(self, conn, addr):
        """
        a function that is connecting to each client, handling the commands from the
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
            print(f"[SERVER] Received command '{command}' with args {args} from {addr}.")
            if command == "validate":
                username, password = args
                dict[username] = conn
                print(dict)
                response = self.Cashit_db.validate_user(username, password)
                response = str(response)
                plen = len(response)
                response = f"{plen}#{response}"
            elif command == "UserExist":
                username = args
                response = self.Cashit_db.user_exist(username)
                response = str(response)
                plen = len(response)
                response = f"{plen}#{response}"

            elif command == "SaveSignupDetails":
                username, password, email, id, sum = args
                self.Cashit_db.save_user(username, password, email, id, sum)
                response = True
                response = str(response)
                plen = len(response)
                response = f"{plen}#{response}"

            elif command == "ReadSignup":
                username = args[0]
                user_data = self.Cashit_db.get_user(username)
                user_data = user_data
                response = user_data
                response = str(response)
                plen = len(response)
                response = f"{plen}#{response}"

            elif command == "permission":
                username, amount, second_user, transfor_name = args
                print("here per")
                socket = dict2[second_user]
                print(socket)
                encryped = self.fernet.encrypt(json.dumps(f"do you agree to {transfor_name} {amount} money - {username}").encode('utf-8'))
                socket.send(encryped)
                response = json.loads(self.fernet.decrypt(socket.recv(200000000)).decode('utf-8'))
                response = str(response)
                if response == "True":
                    self.set_money(username, int(amount))
                    self.set_money(second_user, -1 * int(amount))
                plen = len(response)
                response = f"{plen}#{response}"
                print(response)


            encryped_response = self.fernet.encrypt(json.dumps(response).encode('utf-8'))
            conn.send(encryped_response)
        print(f"[SERVER] Connection with {addr} closed.")
        conn.close()

    def handle_permission(self, conn, addr):
        print("here")
        data = self.fernet.decrypt(conn.recv(config.PACKET_SIZE)).decode('utf-8')
        print("data", data)

        command, args = json.loads(data)
        print(f"[SERVER] Received command '{command}' with args {args} from {addr}.")
        if command == "validate2":
            username, password = args
            dict2[username] = conn
            print(dict2)
            response = self.Cashit_db.validate_user(username, password)
            response = str(response)
            plen = len(response)
            response = f"{plen}#{response}"
            encryped_response = self.fernet.encrypt(json.dumps(response).encode('utf-8'))
            conn.send(encryped_response)

    def get_my_money(self, username):
        """
        a function who gets the money amount from the database by the username
        :param username:
        :return:
        """
        conn = CashitDB().create_connection()

        with conn:
            query = "SELECT * FROM users WHERE username = ?"
            result = conn.execute(query, (username,)).fetchone()
            sum = result[4]
            # return result

        conn.close()
        return sum

    def set_money(self, username, amount):
        # print(username)
        """
        a function who sets the new money amount of each user
        in the database by the username
        """
        current_money = int(self.get_my_money(username))
        updated_money = current_money + amount

        # Validate that user is existed in DB

        if updated_money < 0:
            raise Exception(f"Sorry, you have {current_money} money, you cant pass {amount} :(")

        conn = CashitDB().create_connection()

        with conn:
            query = "UPDATE users SET sum = ? WHERE username = ?"
            result = conn.execute(query, (updated_money, username))
            conn.commit()
            # return result

        conn.close()
        return sum

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

    def validate2(self):
        """
        a function that validate the client from another port and saves the connnection in dict.
        :return:
        """
        self.server2.bind((self.host, self.port2))
        self.server2.listen()
        print(f"[SERVER] Server started on {self.host}:{self.port2}.")

        while True:
            conn, addr = self.server2.accept()
            print("conn, addr", conn, addr)
            thread = threading.Thread(target=self.handle_permission, args=(conn, addr))
            thread.start()
            print(f"[SERVER] Active connections: {threading.active_count() - 1}")

    def handle_bank(self):
        self.server3.bind((self.host, 9000))
        self.server3.listen()
        print(f"[SERVER] Server started on {self.host}:{9000}.")
        while True:
            conn, addr = self.server3.accept()
            print("conn, addr", conn, addr)
            thread = threading.Thread(target=lambda: self.charge_money(conn, addr))
            thread.start()
            print(f"[SERVER] Active connections: {threading.active_count() - 1}")


    def charge_money(self, conn, addr):
        data = conn.recv(config.PACKET_SIZE).decode('utf-8')
        print("data", data)
        command, args = json.loads(data)
        username = command
        print(f"[SERVER] '{command}' with  {args} new money.")
        conn = CashitDB().create_connection()
        updated_money = args
        with conn:
            query = "UPDATE users SET sum = ? WHERE username = ?"
            result = conn.execute(query, (updated_money, username))
            conn.commit()
            # return result


if __name__ == "__main__":
    cashit_server = CashitServer()
    thread1 = threading.Thread(target=cashit_server.start, args=())
    thread1.start()
    thread2 = threading.Thread(target=cashit_server.validate2, args=())
    thread2.start()
    thread3 = threading.Thread(target=cashit_server.handle_bank(), args=())
    thread3.start()

