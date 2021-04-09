import bcrypt
import sqlite3
con = sqlite3.connect('users.db')

def log():
    user = input('Enter username:\n')
    if user_exist(user) == 0:
        print('User not found!\nRetry?')
        retry = input('YES/NO (Y/N)')
        if retry in ['YES', 'yes', 'y', 'Y']:
            main()
        else:
            quit()
    else:
        cur = con.cursor()
        cur.execute('SELECT pass FROM users WHERE user=?', (user,))
        pw2 = input('Enter password:\n')
        if bcrypt.checkpw(pw2.encode('utf-8'), cur.fetchone()[0].encode('utf-8')) == 0:
            print('Wrong password! Retry?')
            while True:
                retry = str(input('YES/NO (Y/N)\n'))
                if retry != '':
                    break
            if retry in ['YES', 'yes', 'y', 'Y']:
                main()
            elif retry in ['NO', 'no', 'n', 'N']:
                quit()
        else:
            print('Nice you\'re logged in! B)')
            input()

def user_exist(user):
    cur = con.cursor()
    cur.execute('SELECT COUNT(user) FROM users WHERE user=?',(user,))
    return cur.fetchall()[0][0]

def register():
    cur = con.cursor()
    user = input('Enter username:\n')
    if user_exist(user):
        print('You are already registered.\n')
        main()
    elif len(user)<3:
        print('Your username must be at least 3 characters!')
        register()
    else:
        pw = input('Enter password:\n')
        result = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
        result = result.decode('utf-8')
        cur.execute(('INSERT INTO users VALUES (?, ?)'), (user, result))
        con.commit()
        print('You are now registered!')
        main()

def change():
    cur = con.cursor()
    user = input('Enter username:\n')
    if user_exist(user):
        old = input('Enter old password:\n')
        cur.execute('SELECT pass FROM users WHERE user=?',(user,))
        if bcrypt.checkpw(old.encode('utf-8'), cur.fetchall()[0][0].encode('utf-8')) == 0:
            print('Wrong password!')
            main()
            return
        else:
            pw = input('Enter new password:\n')
            result = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
            result = result.decode('utf-8')
            cur.execute('UPDATE users SET pass=? WHERE user=?',(result,user))
            con.commit()
            print('Your password has been changed!')
    else:
        print('Name not found!\n')
        main()


def main():
    print("What would you like to do?\n1. Login\n2. Register\n3. Change password\n4. Quit")
    c = int(input('\n\nYour choice: '))
    if c == 1:
        log()
    elif c == 2:
        register()
    elif c == 3:
        change()
    elif c == 4:
        con.close()
        quit()
    else:
        print('Wrong choice...Retry...')
        main()

main()
