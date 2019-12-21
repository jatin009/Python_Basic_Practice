from utils.DatabaseConn import *


def create_table():
    with DatabaseConn('info.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS user_info (account text primary key, username text, password text)')


def add_entry(account_type, name, pwd):

    if not account_type or not name or not pwd:
        print("Empty fields not allowed.")
        return
    
    with DatabaseConn('info.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_info VALUES(?,?,?)', (account_type, name, pwd))

    print("Record successfully added !!!")


def view_entry(account_type):
    with DatabaseConn('info.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, password from user_info WHERE account=?', (account_type,))

        info = {}
        for row in cursor.fetchall():
            info = {'user': row[0], 'pass': row[1]}

    return info


def view_all():
    with DatabaseConn('info.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT account FROM user_info')

        info = [row[0] for row in cursor.fetchall()]

    return info
