from getpass import getpass
from cryptography.fernet import Fernet

from key import get_key
from .db import Db


class User:

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
    
    @classmethod
    def get(cls):
        username = input('Enter your username: ')
        password = getpass('Enter your password: ')
        return cls(username, password)

    def register(self):
        Db.cur.execute('SELECT name FROM Users WHERE name = ?', (self.username,))
        data = Db.cur.fetchone()
        if data is None:
            f = Fernet(get_key())
            encoded_password = self.password.encode()
            encrypted_password = f.encrypt(encoded_password)
            Db.cur.execute('INSERT INTO Users (name, pass) VALUES (?,?)', (self.username, encrypted_password))
            Db.connection.commit()
        else:
            print('Username already exists.')
        print('Success!')

    def login(self):
        Db.cur.execute('SELECT name FROM Users WHERE name = ?', (self.username,))
        data = Db.cur.fetchone()
        if data is None:
            print('You need to register first.')  
            return 'error'
        else:
            Db.cur.execute('SELECT pass FROM Users WHERE name = ?', (self.username,))
            pwd = Db.cur.fetchone()
            f = Fernet(get_key())
            decrypted_pass = f.decrypt(pwd[0])
            decoded_password = decrypted_pass.decode()
            Db.connection.commit()
            if decoded_password == self.password:
                return 'success'
            else:
                print('You\'ve entered a wrong password.')
                return 'error'

    def __str__(self):
        return self.username