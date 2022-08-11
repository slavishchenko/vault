import os
from cryptography.fernet import Fernet

def get_key():
    if not os.path.exists('key.txt'):
        key = Fernet.generate_key()
        with open('key.txt', 'wb') as file:
            file.write(key)
        return key
    else:
        with open('key.txt', 'rb') as file:
            line = file.readlines()
            return line[0]