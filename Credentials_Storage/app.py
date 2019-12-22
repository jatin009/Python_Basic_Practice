import getpass
from utils import database
from cryptography.fernet import Fernet


def encrypt_password(str_pwd):
    with open('info/key.key', 'rb') as file:
        key = file.read()

    encoded = str_pwd.encode()
    f = Fernet(key)
    return f.encrypt(encoded)


def decrypt_password(enc_pwd):
    with open('info/key.key', 'rb') as file:
        key = file.read()

    f = Fernet(key)
    decrypted = f.decrypt(enc_pwd)
    return decrypted.decode()


def get_system_pwd():

    with open('info/system.pwd', 'rb') as file:
        enc_pwd = file.read()

    return decrypt_password(enc_pwd)


def menu():
    system_pwd = getpass.getpass("Hello! Since it's kinda secret app to store credentials, we would like to know "
                                 "it's really you.\nKindly enter the system password: ")

    if system_pwd != get_system_pwd():
        print("Exiting")
        exit()

    option = input("\nGreat! Type 'new' for new entry, 'view' to view the existing record, 'all' or 'quit' to exit: ")

    while option.lower() != 'quit':
        database.create_table()

        if option.lower() == 'new':

            account_type = input('\nYou want to store info for which account (ex- Facebook/Twitter): ')
            user = input("Username: ")
            pwd = ''
            try:
                pwd = getpass.getpass()
            except TypeError:
                print('\nERROR in reading password. Please try again.')
            else:
                database.add_entry(account_type, user, encrypt_password(pwd))

        elif option.lower() == 'view':
            account_type = input('Enter the account for which you want to retrieve info (ex- Facebook/Twitter): ')

            info_dict = database.view_entry(account_type)
            if len(info_dict) > 0:
                print(f"\n\nYour account on \n{account_type} has \n{info_dict['user']} as username and \n{decrypt_password(info_dict['pass'])} as encrypted password.")
                print("\nKindly take the pain to decrypt it yourself :)")
            else:
                print("\nNo record found")

        elif option.lower() == 'all':
            info = database.view_all()

            if len(info) > 0:
                print("\nHere's a list of all your accounts:\n")
                for each_acc in info:
                    print(f"{each_acc}")
            else:
                print("\nNo record at all")

        elif option.lower() == 'quit':
            pass

        option = input("\n\nType 'new' for new entry, 'view' to view the existing record, 'all' or 'quit' to exit: ")


menu()
