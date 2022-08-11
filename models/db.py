import sqlite3
from cryptography.fernet import Fernet

from key import get_key


class Db:
    connection = sqlite3.connect('userdb.sqlite')
    cur = connection.cursor()

    @classmethod
    def create_tables(cls):
        cls.cur.execute('''
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
                name TEXT, 
                pass BLOB
            )'''
        )
        cls.cur.execute('''
            CREATE TABLE IF NOT EXISTS Account (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                uname TEXT, 
                password BLOB, 
                site TEXT, 
                owner INTEGER,
                FOREIGN KEY(owner) REFERENCES User(user_id)
            )'''
        )
    
    @staticmethod
    def encrypt_password(password):
        f = Fernet(get_key())
        encoded_password = password.encode()
        return f.encrypt(encoded_password) 

    @staticmethod
    def decode_password(password):
        f = Fernet(get_key())
        decrypted_password = f.decrypt(password)
        return decrypted_password.decode() 