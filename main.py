import modules.scanner as scanner
import modules.passchecker as passchecker
import sqlite3
from colorama import Fore, Style

def db_creation():

    connection = sqlite3.connect('source/db.db', check_same_thread=False)
    cursor = connection.cursor()

    cursor.executescript('''CREATE TABLE IF NOT EXISTS Hosts (
                        id INTEGER PRIMARY KEY,
                        host TEXT NOT NULL,
                        hostname TEXT,
                        host_state TEXT,
                        protocol TEXT
    );
                        PRAGMA foreign_key=on;
                        CREATE TABLE IF NOT EXISTS Ports (
                        id INTEGER PRIMARY KEY,
                        id_hosts INTEGER,
                        port TEXT NOT NULL,
                        product TEXT,
                        version TEXT,
                        FOREIGN KEY (id_hosts) REFERENCES Hosts (id)
    );''')
    connection.commit()

db_creation()

print('                    ______________        _____ ______ ____ ')
print('                   |   ________   |      / _   |   _  \ ___|')
print('                   | _/  ____  \_ |     / /_|  |  |_\  \    ')
print('                   ( >\ (O  O) /< )    /  __   | ______/___ ')
print('                   ||_/\ \oo/ /\_||   /_/   |__|__| |______|')
print('                   | / /\(==)/\ \ |                         ')
print('                   |/ /###\/###\ \|                         ')
print('                   |\ \########/ /|                         ')
print('                   |______________|                         ')
print('                                                            ')


while True:
    print('Режимы работы:\n[1]{> Сканер открытых портов\n[2]{> Уязвимости\n[3]{> Проверка пароля')
    choise = input(': ')

    match choise:
        case '1':
            scanner.main()
            print(' ')
            input()
        case '2':
            scanner.vuln_check(scanner.vuln_search())
            input()
        case '3':
            password = input('Пароль: ')
            passchecker.passcheck(password)
            print(' ')
            input()
        case 'exit':
            break
        