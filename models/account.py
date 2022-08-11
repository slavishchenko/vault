from getpass import getpass
from cryptography.fernet import Fernet

from .db import Db
from key import get_key


class Account:
    def __init__(self, username, password, website):
        self.username = username
        self.password = password
        self.website = website

    @classmethod
    def get(cls):
        username = input('Username: ')
        password = getpass('Password: ')
        website = input('Website: ')
        return cls(username, password, website)

    def create(self, user):
        f = Fernet(get_key())
        encoded_password = self.password.encode()
        encrypted_password = f.encrypt(encoded_password)

        Db.cur.execute('SELECT id FROM User WHERE name = ?', (user.username,))
        user_id = Db.cur.fetchone()
        Db.cur.execute(
            'INSERT INTO Account (uname, password, site, owner) VALUES (?,?,?,?)',
            (self.username, encrypted_password, self.website, user_id[0])
        )
        Db.connection.commit()

    @staticmethod
    def info():
        username = input('Username: ')
        Db.cur.execute('SELECT password, site FROM Account WHERE uname = ?', (username,))
        data = Db.cur.fetchone()
        if data is None:
            print('Username did not match our records.')
        else:
            password = data[0]
            f = Fernet(get_key())
            decrypted_password = f.decrypt(password)
            decoded_password = decrypted_password.decode()
            print(f'Password: {decoded_password}')
            print(f'Site: {data[1]}')

    @staticmethod
    def search_by_site():
        website = input('Enter the site name: ')
        Db.cur.execute('SELECT uname, password FROM Account WHERE site = ?', (website,))
        data = Db.cur.fetchone()
        if data is None:
            print('There are no records for this site. Please, make sure there are no spelling errors.')
        else:
            password = data[1]
            f = Fernet(get_key())
            decrypted_password = f.decrypt(password)
            decoded_password = decrypted_password.decode()
            print(f'Username: {data[0]}')
            print(f'Password: {decoded_password}')

    @staticmethod
    def see_all(user):
        Db.cur.execute('SELECT * FROM Account WHERE owner = ?', (user.get_id(),))
        data = Db.cur.fetchall()
        if data is None:
            print('You don\'t have any accounts.')
        for account in data:
            print(f'#{account[0]}\nUsername: {account[1]}\nPassword: {account[2]}\nWebsite: {account[3]}\n')

    @staticmethod
    def remove():
        username = input('Enter the username: ')
        Db.cur.execute('DELETE FROM Account WHERE uname = ?', (username,))
        Db.connection.commit()
    