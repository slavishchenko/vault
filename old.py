from getpass import getpass
import time
import os
from cryptography.fernet import Fernet
import sqlite3

if not os.path.exists('key.txt'):
    key = Fernet.generate_key()
    with open('key.txt', 'wb') as file:
        file.write(key)
else:
    with open('key.txt', 'rb') as file:
        line = file.readlines()
        key = line[0]


conn = sqlite3.connect('userdb.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Admins (name TEXT, pass BLOB)')
cur.execute('CREATE TABLE IF NOT EXISTS Users (uname TEXT, password BLOB, site TEXT)')

# welcome screen
def welcome_screen():
    print('Menu:\n\n1. Login \n2. Register \n3. Exit')
    print('\n')
    menu = input('Select an option: ')
    if int(menu) > 3 or int(menu) < 1:
        print('Choose either 1, 2 or 3.')
        welcome_screen()
    try:
        option = int(menu)
    except:
        print('Please enter numeric value')

    if option == 1:
        login()
    elif option == 2:
        register()
    elif option == 3:
        print('Exiting...')
        time.sleep(1)
        quit()
    
# register form
def register():
    username = input('Enter your username: ')
    password = getpass('Enter your password: ')
    cur.execute('SELECT name FROM Admins WHERE name = ?', (username,))
    data = cur.fetchone()
    if data is None:
        f = Fernet(key)
        u_pass = password.encode()
        pword = f.encrypt(u_pass)
        cur.execute('INSERT INTO Admins (name, pass) VALUES (?,?)', (username, pword))
    else:
        print('Username already exists.')
    conn.commit()
    print('Success!')
    main_menu()

# login form
def login():
    username = input('Enter your username: ')
    cur.execute('SELECT name FROM Admins WHERE name = ?', (username,))
    data = cur.fetchone()
    conn.commit()
    if data is None:
        print('You need to register first.')  
        welcome_screen()
    else:
        password = getpass('Enter master password: ')
        pword = cur.execute('SELECT pass FROM Admins WHERE name = ?', (username,))
        pw = cur.fetchone()
        f = Fernet(key)
        upass = f.decrypt(pw[0])
        user_p = upass.decode()
        conn.commit()
        if user_p == password:
            print('Login successful.')
            time.sleep(.30)
            print('\n')
            main_menu()
        else:
            print('You\'ve entered a wrong password.')
            print('\n')
            welcome_screen()
    conn.commit()

# create a menu
def main_menu():
    print('\nMenu:\n\n1. Add a new account \n2. Look up an account \n3. Search by site \n4. Remove an account \n5. Exit')
    print('\n')
    menu = input('Choose an option: ')
    # menu selection validation
    try:
        option = int(menu)
    except:
        print('Invalid input. Please, enter 1 or 2\nRun the program again.')
        quit()

    if option == 1:
        add_account()
        print('Account saved!')
        print('\n')
        return_to_top_menu()
    elif option == 2:
        find_account_info()
        return_to_top_menu()
    elif option == 3:
        search_by_the_site()
        return_to_top_menu()
    elif option == 4:
        remove_account()
        print('Account removed!')
        print('\n')
        return_to_top_menu()
    elif option == 5:
        quit()
    else:
        print('Please choose either 1 or 2\nRun the program again.')
        quit()

 
def add_account():   
    userName = input('Username: ')
    passWord = getpass('Password: ')
    f = Fernet(key)
    u_pass = passWord.encode()
    pword = f.encrypt(u_pass)
    site = input('Website: ')
    cur.execute('INSERT INTO Users (uname, password, site) VALUES (?,?,?)', (userName, pword, site))
    conn.commit()
        
def find_account_info():
    name = input('Enter the username: ')
    cur.execute('SELECT password, site FROM Users WHERE uname = ?', (name,))
    data = cur.fetchone()
    if data is None:
        print('Username did not match our records.')
    else:
        password = data[0]
        f = Fernet(key)
        upass = f.decrypt(password)
        pw = upass.decode()
        print('Password: ' + pw)
        print('Site: ' + data[1])

def search_by_the_site():
    site = input('Enter the site name: ')
    cur.execute('SELECT uname, password FROM Users WHERE site = ?', (site,))
    data = cur.fetchone()
    if data is None:
        print('There are no records for this site. Please, make sure there are no spelling errors.')
    else:
        password = data[1]
        f = Fernet(key)
        upass = f.decrypt(password)
        pw = upass.decode()
        print('Username: ' + data[0])
        print('Password: ' + pw)
        
                
def remove_account():
    name = input('Enter the username: ')
    cur.execute('DELETE FROM Users WHERE uname = ?', (name,))
    conn.commit()
                    
def return_to_top_menu():
    print('Menu:\n\n1. Back to top menu \n2. Exit')
    print('\n')
    menu = input('Choose an option: ')
    # menu selection validation
    try:
        option = int(menu)
    except:
        print('Invalid input.')
        quit()

    if option == 1:
        main_menu()    
    elif option == 2:
        quit()
    else:
        print('Invalid input')
        quit()
        
welcome_screen()

cur.close()



# from User register method
# Db.cur.execute('SELECT name FROM Users WHERE name = ?', (self.username,))
# data = Db.cur.fetchone()
# if data is None:
#     f = Fernet(get_key())
#     u_pass = self.password.encode()
#     pword = f.encrypt(u_pass)
#     Db.cur.execute('INSERT INTO Users (name, pass) VALUES (?,?)', (self.username, pword))
#     Db.connection.commit()
# else:
#     print('Username already exists.')
# print('Success!')