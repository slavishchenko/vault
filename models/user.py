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
        Db.cur.execute('SELECT name FROM User WHERE name = ?', (self.username,))
        data = Db.cur.fetchone()
        if data is None:
            encrypted_password = Db.encrypt_password(self.password)
            Db.cur.execute('INSERT INTO User (name, pass) VALUES (?,?)', (self.username, encrypted_password))
            Db.connection.commit()
        else:
            print('Username already exists.')
        print('Success!')

    def login(self):
        Db.cur.execute('SELECT name FROM User WHERE name = ?', (self.username,))
        name = Db.cur.fetchone()
        if name is None:
            print('You need to register first.')  
            return 'error'
        else:
            Db.cur.execute('SELECT pass FROM User WHERE name = ?', (self.username,))
            password = Db.cur.fetchone()[0]
            decoded_password = Db.decode_password(password)
            Db.connection.commit()
            if decoded_password == self.password:
                return 'success'
            else:
                print('You\'ve entered a wrong password.')
                return 'error'
                
    def get_id(self):
        Db.cur.execute('SELECT id FROM User WHERE name = ?', (self.username,))
        return Db.cur.fetchone()[0]

    def __str__(self):
        return self.username