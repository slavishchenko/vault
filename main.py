from models.user import User
from models.account import Account
from models.db import Db
from validators import is_valid_input


def main():
	Db.create_tables()
	OPTIONS = [x for x in range(1, 4)]

	menu = input('Menu:\n\n1. Login \n2. Register \n3. Exit\n')

	if is_valid_input(menu, OPTIONS):
		selected_option = int(menu)
		match selected_option:
			case 1:
				user = User.get()
				if User.login(user) == 'error':
					main()
				else:
					print('Login successfull')
					main_menu(user)
			case 2:
				user = User.get()
				User.register(user)
			case 3:
				print('Exiting...')
				quit()
	else:
		print('Invalid input')
		main()

def main_menu(user):
	OPTIONS = [x for x in range(1,7)]
	print(f'Currently logged in as: {user}')
	menu = input(
		'''
\nMenu:\n\n
1. Add a new account \n
2. Look up an account \n
3. Search by site \n
4. Remove an account \n
5. See all accounts \n
6. Exit\n
		'''
	)
	
	if is_valid_input(menu, OPTIONS):
		selected_option = int(menu)

		match selected_option:
			case 1:
				account = Account.get()
				Account.create(account)
				print('Account saved!')
				print('\n')
				return_to_top_menu()
			case 2:
				Account.info()
				return_to_top_menu()
			case 3:
				Account.search_by_site()
				return_to_top_menu()
			case 4:
				Account.remove()
				print('Account removed!')
				print('\n')
				return_to_top_menu()
			case 5:
				Account.see_all()
				print('\n')
				return_to_top_menu()
			case 6:
				quit()
	else:
		print('Please, enter a numeric value')


def return_to_top_menu():
	OPTIONS = [x for x in range(1, 3)]
	menu = input('Menu:\n\n1. Back to top menu \n2. Exit\n')

	if is_valid_input(menu, OPTIONS):
		selected_option = int(menu)

		match selected_option:
			case 1:
				main_menu()    
			case 2:
				quit()


if __name__ == '__main__':
	main()
	Db.cur.close()