import sqlite3


class Db:
    connection = sqlite3.connect('userdb.sqlite')
    cur = connection.cursor()

    @classmethod
    def create_tables(cls):
        cls.cur.execute('CREATE TABLE IF NOT EXISTS Users (name TEXT, pass BLOB)')
        cls.cur.execute('CREATE TABLE IF NOT EXISTS Accounts (uname TEXT, password BLOB, site TEXT)')
    