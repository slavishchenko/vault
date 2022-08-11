import os
from cryptography.fernet import Fernet

def get_key():
    if not os.path.exists('key.key'):
        key = Fernet.generate_key()
        with open('key.key', 'wb') as file:
            file.write(key)
        return key
    else:
        with open('key.key', 'rb') as file:
            line = file.readlines()
            return line[0]