"""
author - lihi
date   - 29 / 05 / 23
DB
"""
#file name CashitDB.py

import sqlite3
import config
from sqlite3 import Error


class CashitDB:
    def __init__(self):
        self.db_file = config.DB_FILE_PATH

    def create_connection(self):
        """
        a function who creates the connection to the database
        :return:
        """
        conn = None;
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        return conn

    def create_tables(self):
        """
        a function that creates the tables of the database who
         saves all the data
        :return:
        """
        conn = self.create_connection()
        with conn:
            users_table = '''CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY,
                                password TEXT NOT NULL,
                                email TEXT NOT NULL,
                                id TEXT NOT NULL,
                                sum TEXT NOT NULL
                             );'''

            conn.execute(users_table)

    def save_user(self, username, password, email, id, sum):
        """
        a function that saves the new user in the database
        :param username:
        :param password:
        :param email:
        :param id:
        :param sum:
        :return:
        """
        conn = self.create_connection()

        with conn:
             query = "INSERT INTO users (username, password, email, id, sum) VALUES (?, ?, ?, ?, ?)"
             conn.execute(query, (username, password, email, id, sum))

    def validate_user(self, username, password):
        """
        a function that checks if the user is exists and the password is correct
        :param username:
        :param password:
        :return:
        """
        conn = self.create_connection()
        with conn:
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            result = conn.execute(query, (username, password)).fetchone()
            return result is not None

    def user_exist(self, username):
        """
        a function that checks if the user is exists
        :param username:
        :return:
        """
        conn = self.create_connection()
        with conn:
            query = "SELECT * FROM users WHERE username = ?"
            result = conn.execute(query, username).fetchone()
            return result is not None

    def get_user(self, username):
        """
        a function who gets all the data of a user by his username from the DB
        :param username:
        :return:
        """
        conn = self.create_connection()
        with conn:
            query = "SELECT * FROM users WHERE username = ?"
            result = conn.execute(query, (username,)).fetchone()
            return result
