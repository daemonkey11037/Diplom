import modules.scanner as scanner
import modules.passchecker as passchecker
import sqlite3
from colorama import Fore, Style



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
    print('''Режимы работы:\n
          [1]{> Сканер открытых портов\n
          [2]{> Уязвимости\n
          [3]{> Проверка пароля''')
    choise = input(': ')

    match choise:
        case '1':
            scanner.main()
            print(' ')
            input('Нажмите Enter...')
        case '2':
            scanner.vuln_check(scanner.vuln_search())
            input('Нажмите Enter...')
        case '3':
            password = input('Пароль: ')
            passchecker.passcheck(password)
            print(' ')
            input('Нажмите Enter...')
        case 'exit':
            break
        